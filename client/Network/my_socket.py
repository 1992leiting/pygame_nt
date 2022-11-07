import json
import threading
import time
from Common.socket_id import *
from Common.common import show_error
from Common.constants import game


class SocketClient:
    def __init__(self, socket, director):
        super(SocketClient, self).__init__()
        self.socket = socket
        self.tmp_str = ''
        self.enable = False

    def start(self):
        thread = threading.Thread(target=self.recv_data, daemon=True)
        thread.start()

    def recv_data(self):
        """
        socket.recv获取是阻塞的
        :return:
        """
        while True:
            try:
                _bytes = self.socket.recv(2)  # 阻塞获取2字节, 如果有则是消息长度
                msg_len = int.from_bytes(_bytes, byteorder='big')  # 消息长度, 2字节
                recv_len = 0
                msg = b''
                while recv_len < msg_len:
                    msg += self.socket.recv(msg_len - recv_len)  # 获取消息内容
                    recv_len += len(msg)
                # print('***msg_len', _bytes, msg_len, len(msg))
                # print('***msg', msg)
                self.recv_handler(msg)
            except BaseException as e:
                raise e
                # show_error('接收服务器数据异常, 请尝试重新登陆', '网络错误')
                # print('recv data error:', str(e))

    def recv_handler(self, recv_bytes):
        data = json.loads(recv_bytes)
        # print('socket收到:', data)
        cmd = data['cmd']
        if cmd == '登陆成功':
            self.send('获取全部角色数据', {})
        elif cmd == S_角色数据:
            game.director.char_data = data
            print('角色数据:', game.director.char_data)
        elif cmd == '添加NPC':
            # while not game.director.STARTED:
            #     pass
            world = game.director.child('world')
            world.add_npc(data)
        elif cmd == '跳转地图':
            game.director.HERO_IN_PORTAL = 0
            hero = game.director.child('world').child('hero')
            hero.path = []
            hero.is_moving = False
            hero.game_x, hero.game_y = int(data['x']), int(data['y'])
            world = game.director.child('world')
            world.change_map(int(data['mapid']))
        elif cmd == S_系统提示:
            print('系统提示:', data)
            text = data['内容']
            game.director.gp_manager.append(text)

    def send(self, cmd: str, send_data: dict):
        send_data['cmd'] = cmd
        json_str = json.dumps(send_data)
        json_str_len = len(json_str)
        len_bytes = json_str_len.to_bytes(2, byteorder='big')
        send_bytes = len_bytes + json_str.encode(encoding='utf-8')
        try:
            self.socket.sendall(send_bytes)
        except:
            show_error('发送网络数据失败, 请尝试重新登陆', '网络错误')
