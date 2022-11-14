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


class GameServer(threading.Thread):
    def __init__(self):
        super(GameServer, self).__init__()
        self.players = []  # 存放所有在此game server维护的玩家id
        self.uuid = short_uuid()
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
                    # try:
                    self.recv_handler(msg)
                    # except Exception as e:
                    #     sprint('Game Server处理业务时发生错误:' + str(e))
            except ConnectionResetError as e:
                sprint('接收服务器数据异常, 请尝试重新登陆:' + str(e))
                exit()
            except BaseException as e:
                print(e)
                print(traceback.print_exc())
                # raise e

    def recv_handler(self, recv_bytes):
        msg = json.loads(recv_bytes)
        pid = msg['pid']  # 玩家id
        cmd = msg['cmd']
        # print('game server recv:', msg)

        if cmd == C_更新坐标:
            x, y = msg['x'], msg['y']
            rset(pid, CHAR, x, 'mx')
            rset(pid, CHAR, y, 'my')
        elif cmd == C_进入场景:
            from scene.scene_handler import player_enter_scene
            map_id = msg['map_id']
            player_enter_scene(pid, map_id)


def start_game_server():
    redis_client = RedisClient()
    server.redis_conn = redis_client.conn

    game_server = GameServer()
    server.game_server = game_server
    game_server.connect()
    game_server.start()

    send2gw(GAME_SERVER_REGISTER_CMD, dict(uuid=game_server.uuid))
    # import_npcs()


start_game_server()
