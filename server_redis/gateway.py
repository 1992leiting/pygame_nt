import orjson

from common.server_process import server, RedisClient
from common.common import *
from common.constants import *
import threading
import socketserver
import os
from common.socket_id import *


class PlayerClient:
    """
    玩家socket链接, 记录了对应的账号,pid,socket和game server
    """
    def __init__(self, acc, pid, socket, server):
        self.pid = pid
        self.account = acc
        self.socket = socket
        self.game_server = server


class GatewayServer(socketserver.BaseRequestHandler):
    lock = threading.Lock()
    event = None
    clients = {}  # 所有连接socket的客户端
    game_servers = []  # 所有的游戏服务器链接
    players = {}  # 所有的玩家链接 key: socket, value: PlayerClient

    def setup(self) -> None:
        super(GatewayServer, self).setup()
        self.event = threading.Event()
        with self.lock:
            self.clients[self.client_address] = self.request
        # print('新加入一个连接{}, 当前连接数量:{}'.format(self.client_address, len(self.clients)))

    def get_pid_socket(self, pid):
        for player_client in self.players:
            if pid == player_client.pid:
                return player_client.socket
        return None

    def handle(self) -> None:
        from common.common import sprint
        super(GatewayServer, self).handle()
        while not self.event.is_set():
            try:
                data = self.request.recv(2)  # 2字节的data_len
                data_len = int.from_bytes(data, byteorder='big')
                data = self.request.recv(data_len)  # data_len字节的内容
                msg = orjson.loads(data)
                # print('msg:', msg)
                tp = msg['cmd']
            except:
                self.event.set()
                sprint('client离线:{}'.format(self.client_address))
                break

            gateway_socket.cur_socket = self.request
            # game server进程注册
            if tp == GAME_SERVER_REGISTER_CMD:
                uuid = msg['uuid']
                if self.request not in self.game_servers:
                    # self.game_servers[uuid] = {
                    #     'socket': self.request,  # game server进程的socket
                    # }
                    # sprint('Game Server接入:{}'.format(self.client_address))
                    self.game_servers.append(self.request)
                    print(self.game_servers)
            # 来自game_server, 转发
            if self.request in self.game_servers:
                player_socket = self.get_pid_socket(msg['pid'])
                send(player_socket, msg['cmd'], msg)
            # 来自已登录玩家,直接转发给对应的game server
            elif self.request in self.players:
                msg['pid'] = self.players[self.request].pid
                msg['account'] = self.players[self.request].account
                send(self.players[self.request].game_server, tp, msg)
            # 其他
            else:
                if tp == C_创建账号:
                    account = msg['账号']
                    passwd = msg['密码']
                    from system.system_handler import create_account
                    from player.player_handler import create_player
                    create_account(account, passwd)
                    create_player(account, '飞龙在天', '龙太子')
                elif tp == C_创建角色:
                    account = msg['账号']
                    name = msg['名称']
                    model = msg['模型']
                    from player.player_handler import create_player
                    create_player(account, name, model)
                elif tp == C_登陆:
                    account = msg['账号']
                    passwd = msg['密码']
                    pid = msg['pid']
                    from player.player_handler import player_login
                    if player_login(account, passwd, pid):
                        # TODO: 登陆成功则分配game server
                        self.players[self.request] = PlayerClient(account, pid, self.request, self.game_servers[0])


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

    # 连接redis并清除数据
    redis_client = RedisClient()
    server.redis_conn = redis_client.conn
    server.redis_conn.flushall()

    sprint('启动子进程...')
    # os.system('start python')
    os.system('start python redis_server.py')
    os.system('start python game_server.py')
    os.system('start python game_server.py')
    os.system('start python game_server.py')

    while True:
        try:
            cmd = input('')
        except:
            break
