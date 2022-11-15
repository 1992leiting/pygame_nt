from common.server_process import server, RedisClient
from redis_server import RedisServer
from common.common import *
from common.constants import *
import threading
import socketserver
import os
from common.socket_id import *
from system.system_handler import *


class PlayerClient:
    """
    玩家socket链接, 记录了对应的账号,pid,socket和game server
    """
    def __init__(self, acc, pid, socket):
        self.pid = pid  # 玩家id
        self.account = acc  # 账户
        self.socket = socket  # socket
        self.game_server = None


class GameServerClient:
    def __init__(self, uid, socket):
        self.uid = uid  # 唯一id
        self.socket = socket  # game server进程的socket
        self.players = []  # 在这个game server进程处理的玩家id

    @property
    def weight(self):
        return len(self.players)


class GatewayServer(socketserver.BaseRequestHandler):
    lock = threading.Lock()
    event = None
    clients = {}  # 所有连接socket的客户端
    game_servers = {}  # 所有的游戏服务器链接
    players = {}  # 所有的玩家链接 key: socket, value: PlayerClient

    def setup(self) -> None:
        super(GatewayServer, self).setup()
        self.event = threading.Event()
        with self.lock:
            self.clients[self.client_address] = self.request
        # print('新加入一个连接{}, 当前连接数量:{}'.format(self.client_address, len(self.clients)))

    def get_pid_socket(self, pid):
        """
        根据玩家id返回其对应的客户端socket
        :param pid:
        :return:
        """
        for player_client in self.players.values():
            if pid == player_client.pid:
                return player_client.socket
        return None

    def assign_server_to_player(self, p: PlayerClient):
        # 分配人数最少的game server给当前player
        game_server_client = sorted(self.game_servers.values(), key=lambda x: x.weight)[0]
        game_server_client.players.append(p.pid)
        p.game_server = game_server_client.socket

    def handle(self) -> None:
        from common.common import sprint
        super(GatewayServer, self).handle()
        while not self.event.is_set():
            try:
                data = self.request.recv(2)  # 2字节的data_len
                data_len = int.from_bytes(data, byteorder='big')
                msg = b''
                while len(msg) < data_len:
                    msg += self.request.recv(data_len - len(msg))  # data_len字节的内容
                msg = json.loads(msg)
                tp = msg['cmd']
            except:
                self.event.set()
                sprint('client离线:{}'.format(self.client_address))
                self.client_out(self.request)
                break

            # game server进程注册
            if tp == GAME_SERVER_REGISTER_CMD:
                uid = msg['uuid']
                if self.request not in self.game_servers:
                    self.game_servers[self.request] = GameServerClient(uid, self.request)
                    sprint('Game server接入:{}'.format(uid))
            # msg来自game_server, 转发给对应的player socket
            elif self.request in self.game_servers:
                # print('来自game server:', msg)
                player_socket = self.get_pid_socket(int(msg['pid']))
                if not player_socket:
                    print('player socket未找到:', msg['pid'])
                send(player_socket, msg['cmd'], msg)
            # 来player socket,直接转发给对应的game server
            elif self.request in self.players:
                msg['pid'] = int(self.players[self.request].pid)
                msg['account'] = self.players[self.request].account
                send(self.players[self.request].game_server, tp, msg)
            # 其他为注册的socket
            else:
                if tp == C_创建账号:
                    account = msg['账号']
                    passwd = msg['密码']
                    server.tmp_client_socket[account] = self.request
                    from system.system_handler import create_account
                    from player.player_handler import create_player
                    create_account(account, passwd)
                elif tp == C_创建角色:
                    account = msg['账号']
                    name = msg['名称']
                    model = msg['模型']
                    server.tmp_client_socket[account] = self.request
                    from player.player_handler import create_player
                    create_player(account, name, model)
                elif tp == C_账号登陆:
                    account = msg['账号']
                    passwd = msg['密码']
                    server.tmp_client_socket[account] = self.request
                    if account_login(account, passwd):
                        server.logged_socket.append(self.request)
                elif tp == C_创建角色:
                    from player.player_handler import create_player
                    account = msg['账号']
                    model = msg['模型']
                    name = msg['名称']
                    server.tmp_client_socket[account] = self.request
                    if self.request in server.logged_socket:  # 检查是否已登录
                        create_player(account, name, model)
                elif tp == C_角色进入:
                    from player.player_handler import player_login
                    account = msg['账号']
                    pid = msg['pid']
                    server.tmp_client_socket[account] = self.request
                    if player_login(account, pid):
                        self.players[self.request] = PlayerClient(account, pid, self.request)
                        self.assign_server_to_player(self.players[self.request])  # 分配服务端
                    print('有角色进入:', self.players)

    def client_out(self, socket):
        """
        连接离线处理
        :param socket:
        :return:
        """
        # 如果game server掉线
        if socket in self.game_servers:
            pass
        # 如果玩家离线
        elif socket in self.players:
            player = self.players[socket]
            print('{}已离线'.format(player.pid))
            # 已登录账号中去除
            server.logged_socket.remove(socket)
            # 从game server里删除这个玩家
            for s in self.game_servers.values():
                if player.pid in s.players:
                    s.players.remove(player.pid)
            # 从self.players中删除这个socket
            del self.players[socket]
            # 保存玩家数据
            server.redis_server.redis_save(player.pid)
            # 从redis中删除这个玩家
            server.redis_server.remove(player.pid)
            # Test: 打印所有game server的pid
            for s in self.game_servers.values():
                print('Game server:', s.uid, s.players)


def start_tcp_server():
    """
    开启TCP服务器, 每个连接以线程方式运行
    :return:
    """
    gateway_server.daemon_threads = True
    threading.Thread(target=gateway_server.serve_forever, name='GATEWAY', daemon=True).start()


if __name__ == '__main__':
    # 启动网关tcp服务
    gateway_server = socketserver.ThreadingTCPServer(GATEWAY_SERVER, GatewayServer)  # 网关进程
    server.gateway = gateway_server
    start_tcp_server()
    sprint('网关启动成功')

    # 启动redis监控线程
    redis_server = RedisServer()
    redis_server.setup()
    server.redis_server = redis_server
    redis_server.start()

    # 连接redis并清除数据
    redis_client = RedisClient()
    server.redis_conn = redis_client.conn
    server.redis_conn.flushall()

    sprint('启动子进程...')
    # os.system('start python')
    # os.system('start python redis_server.py')
    os.system('start python game_server.py')
    os.system('start python game_server.py')
    os.system('start python game_server.py')

    while True:
        try:
            cmd = input('')
        except:
            break
