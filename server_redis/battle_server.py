from common.server_process import server, RedisClient
from common.common import *
from common.constants import *
import threading
import socket
from uuid import uuid4
from common.socket_id import *
import sys
import logging
import traceback
from scene.scene_handler import *
from scene.dialog_handler import *
from player.player_handler import *


uuidChars = ("a", "b", "c", "d", "e", "f",
             "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
             "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
             "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
             "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z")


def short_uuid():
    uuid = str(uuid4()).replace('-', '')
    result = ''
    for i in range(0,8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += uuidChars[x % 0x3E]
    return result


class BattleServer(threading.Thread):
    def __init__(self):
        super(BattleServer, self).__init__()
        self.battles = []  # 存放所有在此battle对象
        self.uuid = short_uuid()
        self.socket = socket.socket()

    def connect(self):
        """
        只有battle server进程才进行connect
        :return:
        """
        self.socket.connect(('127.0.0.1', 9093))

    def run(self):
        from common.common import sprint
        sprint('battle server进程启动...')
        while True:
            try:
                _bytes = self.socket.recv(4)  # 阻塞获取2字节, 如果有则是消息长度
                msg_len = int.from_bytes(_bytes, byteorder='big')  # 消息长度, 2字节
                msg = b''
                while len(msg) < msg_len:
                    msg += self.socket.recv(msg_len - len(msg))  # 获取消息内容
                self.recv_handler(msg)
            except ConnectionResetError as e:
                sprint('接收服务器数据异常, 请尝试重新登陆:' + str(e))
                exit()
            except BaseException as e:
                print(e)
                print(traceback.print_exc())
                # raise e

    def recv_handler(self, recv_bytes):
        pass


def start_battle_server():
    redis_client = RedisClient()
    server.redis_conn = redis_client.conn

    battle_server = BattleServer()
    server.battle_server = battle_server
    battle_server.connect()
    battle_server.start()

    send2gw(BATTLE_SERVER_REGISTER_CMD, dict(uuid=battle_server.uuid), 1)


start_battle_server()
