import json
import numpy
import threading
import time
from Common.socket_id import *
from Common.common import show_error
from Common.constants import *


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


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
                msg = b''
                while len(msg) < msg_len:
                    msg += self.socket.recv(msg_len - len(msg))  # 获取消息内容
                self.recv_handler(msg)
            except BaseException as e:
                raise e
                # show_error('接收服务器数据异常, 请尝试重新登陆', '网络错误')
                # print('recv data error:', str(e))

    def recv_handler(self, recv_bytes):
        # print('recv bytes:', recv_bytes)
        try:
            msg = json.loads(recv_bytes)
        except BaseException as e:
            print('socket接收数据解析错误:', str(e), recv_bytes)
            return
        cmd = msg['cmd']
        if cmd == S_登陆成功:
            print('登陆成功')
            game.director.hero_data = msg
            game.director.start_game()
        elif cmd == S_角色数据:
            game.director.hero_data = msg
            print('角色数据:', game.director.hero_data)
        elif cmd == S_账号所有人物:
            win = game.director.get_node('window_layer/简易选择角色')
            win.switch(True)
            win.load_hero_data(msg['内容'])
            game.account = msg['账号']
        elif cmd == S_NPC数据:
            game.world.add_npc(msg)
        elif cmd == S_玩家数据:
            game.world.add_player(msg)
        elif cmd == '跳转地图':
            game.director.HERO_IN_PORTAL = 0
            hero = game.director.child('world').child('hero')
            hero.path = []
            hero.is_moving = False
            hero.game_x, hero.game_y = int(msg['x']), int(msg['y'])
            world = game.director.child('world')
            world.change_map(int(msg['mapid']))
        elif cmd == S_系统提示:
            print('系统提示:', msg)
            text = msg['内容']
            game.director.gp_manager.append(text)
        elif cmd == S_发送路径:
            path = msg['路径']
            game.hero.set_path(path)
        elif cmd == S_玩家寻路:
            pid = msg['玩家']
            path = msg['路径']
            game.world.player_set_path(pid, path)
        elif cmd == S_频道发言:
            ch = msg['频道']
            text = msg['内容']
            name = msg['名称']
            added_text = '{}#W[{}] {}'.format(CHL_CODE[ch], name, text)
            game.world_msg_flow.append_text(added_text)
        elif cmd == S_角色发言显示:
            pid = msg['player']
            text = msg['内容']
            game.world.player_add_speech_prompt(pid, text)

    def send(self, cmd: str, send_data: dict):
        send_data['cmd'] = cmd
        try:
            json_str = json.dumps(send_data, cls=MyEncoder)
        except BaseException as e:
            print('发送数据解析错误:', send_data, str(e))
            return
        json_str_len = len(json_str)
        len_bytes = json_str_len.to_bytes(2, byteorder='big')
        send_bytes = len_bytes + json_str.encode(encoding='utf-8')
        try:
            self.socket.sendall(send_bytes)
        except:
            show_error('发送网络数据失败, 请尝试重新登陆', '网络错误')
            exit()
