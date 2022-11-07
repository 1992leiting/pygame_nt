import socketserver
import threading
import orjson
from common.common import send
from common.constants import *
from common.socket_id import *
from common.constants import gateway_socket
import socket
import redis
import time
import os


class GatewayServer(socketserver.BaseRequestHandler):
    lock = threading.Lock()
    event = None
    clients = {}  # 所有连接socket的客户端
    game_servers = {}  # 所有的游戏服务器链接, key: socket
    players = {}  # 所有的玩家链接 key: pid

    def setup(self) -> None:
        super(GatewayServer, self).setup()
        self.event = threading.Event()
        with self.lock:
            self.clients[self.client_address] = self.request
        # print('新加入一个连接{}, 当前连接数量:{}'.format(self.client_address, len(self.clients)))

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
            if tp == GAME_SERVER_REGISTER_CMD:
                if self.request not in self.game_servers:
                    self.game_servers[self.request] = {
                        'client_num': 0,  # 玩家数量
                    }
                    sprint('Game Server接入:{}'.format(self.client_address))
                    print(self.game_servers)
            elif tp == C_创建账号:
                account = msg['账号']
                passwd = msg['密码']
                from system.system_handler import create_account
                create_account(account, passwd)
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
                player_login(account, passwd, pid)


class RedisServer(threading.Thread):
    def __init__(self):
        super(RedisServer, self).__init__()
        self.conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
        self.timer = time.time() + REDIS_AUTO_SAVE_INTERVAL

    def setup(self):
        from common.common import dict2file, file2dict, redis_set_data
        # 没有account summary file则创建
        account_summary_file = os.path.join(DATA_PATH, 'account_summary.json')
        if not os.path.exists(account_summary_file):
            data = {}
            dict2file(data, account_summary_file)
        # 读取account summary
        data = file2dict(account_summary_file)
        redis_set_data(self.conn, 'account_summary', data)

    def run(self):
        from common.common import sprint
        sprint('redis watcher启动...')
        while True:
            if time.time() > self.timer:
                self.timer = time.time() + REDIS_AUTO_SAVE_INTERVAL
                self.save()

    def redis_save(self, key):
        from common.common import redis_get_data, dict2file, redis_get_hash_data
        if key == 'account_summary':
            data = redis_get_data(self.conn, key)
            dict2file(data, ACCOUNT_SUMMARY_PATH)
        else:  # 玩家数据数据
            pid = key
            # 角色数据
            data = redis_get_hash_data(self.conn, key, 'char')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'char.json')
            dict2file(data, file)
            # 物品数据
            data = redis_get_hash_data(self.conn, key, 'item')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'item.json')
            dict2file(data, file)
            # 物品仓库数据
            data = redis_get_hash_data(self.conn, key, 'item_warehouse')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'item_warehouse.json')
            dict2file(data, file)
            # 宠物数据
            data = redis_get_hash_data(self.conn, key, 'pet')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'pet.json')
            dict2file(data, file)
            # 宠物仓库数据
            data = redis_get_hash_data(self.conn, key, 'pet_warehouse')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'pet_warehouse.json')
            dict2file(data, file)

    def save(self, key=None):
        """
        redis数据落盘
        :return:
        """
        from common.common import sprint
        if key:  # 指定key保存数据
            self.redis_save(key)
        else:  # 未指定key保存所有
            for key in self.conn.keys():
                self.redis_save(key)
        sprint('redis数据已保存')


class RedisClient:
    def __init__(self):
        self.conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


class GameServerClient(threading.Thread):
    def __init__(self):
        super(GameServerClient, self).__init__()
        self.players = []  # 存放所有在此game server维护的玩家id
        self.socket = socket.socket()

    def connect(self):
        """
        只有game server进程才进行connect
        :return:
        """
        self.socket.connect(('127.0.0.1', 9093))

    def run(self):
        from common.common import sprint
        sprint('game server进程启动...')
        while True:
            try:
                _bytes = self.socket.recv(2)  # 阻塞获取2字节, 如果有则是消息长度
                msg_len = int.from_bytes(_bytes, byteorder='big')  # 消息长度, 2字节
                recv_len = 0
                msg = b''
                while recv_len < msg_len:
                    msg += self.socket.recv(msg_len - recv_len)  # 获取消息内容
                    recv_len += len(msg)
                self.recv_handler(msg)
            except BaseException as e:
                sprint('接收服务器数据异常, 请尝试重新登陆:' + str(e))
                _ = input('Press any key to exit...')

    def recv_handler(self, recv_bytes):
        data = orjson.loads(recv_bytes)
        pid = data['pid']  # 玩家id
        cmd = data['cmd']


game_server_client = GameServerClient()  # game server进程
redis_server = RedisServer()  # redis监控进程
redis_client = RedisClient()  # 每个进程的redis连接
