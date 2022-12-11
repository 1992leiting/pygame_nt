from common.common import *
from common.constants import *
import threading
import socketserver
import os
from common.socket_id import *
from system.system_handler import *
from game_server import *


class PlayerClient:
    """
    玩家socket链接, 记录了对应的账号,pid,socket和game server
    """
    def __init__(self, acc, pid, socket):
        self.pid = pid  # 玩家id
        self.account = acc  # 账户
        self.socket = socket  # socket


class GatewayServer(socketserver.BaseRequestHandler):
    lock = threading.Lock()
    event = None
    clients = {}  # 所有连接socket的客户端
    logged_clients = []
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

    def handle(self) -> None:
        from common.common import sprint
        super(GatewayServer, self).handle()
        while not self.event.is_set():
            try:
                data = self.request.recv(4)  # 4字节的data_len
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

            # 来player socket,直接转发给对应的game server
            if self.request in self.players:
                msg['pid'] = int(self.players[self.request].pid)
                msg['account'] = self.players[self.request].account
                player_cmd_handler(msg)
            # 其他为注册的socket
            else:
                if tp == C_创建账号:
                    account = msg['账号']
                    passwd = msg['密码']
                    server.tmp_client_socket[account] = self.request
                    from system.system_handler import create_account
                    from player.player_handler import create_player
                    create_account(self.request, account, passwd)
                elif tp == C_创建角色:
                    account = msg['账号']
                    name = msg['名称']
                    model = msg['模型']
                    server.tmp_client_socket[account] = self.request
                    from player.player_handler import create_player
                    create_player(self.request, account, name, model)
                elif tp == C_账号登陆:
                    account = msg['账号']
                    passwd = msg['密码']
                    if account_login(self.request, account, passwd):
                        self.logged_clients.append(self.request)
                elif tp == C_创建角色:
                    from player.player_handler import create_player
                    account = msg['账号']
                    model = msg['模型']
                    name = msg['名称']
                    server.tmp_client_socket[account] = self.request
                    if self.request in self.logged_clients:  # 检查是否已登录
                        create_player(self.request, account, name, model)
                elif tp == C_角色进入:
                    from player.player_handler import player_login
                    account = msg['账号']
                    pid = msg['pid']
                    if player_login(self.request, account, pid):
                        self.players[self.request] = PlayerClient(account, pid, self.request)
                    print('有角色进入:', self.players)

    def client_out(self, sk):
        """
        连接离线处理
        :param socket:
        :return:
        """
        # 如果玩家离线
        if sk in self.players:
            player = self.players[sk]
            print('{}已离线'.format(player.pid))
            # 已登录账号中去除
            self.logged_clients.remove(sk)
            # 从self.players中删除这个socket
            del self.players[sk]
            # 保存玩家数据
            save_player_data(player.pid)
            # Test: 打印所有game server的pid



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

    while True:
        try:
            cmd = input('')
        except:
            break
