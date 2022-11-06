from Common.socket_id import *
import numpy as np
import datetime
import socket
import json
import os
import pickle
import time
import pandas as pd
from multiprocessing import Process
from Common.constants import *
import time


def sprint(text: str):
    t = time.gmtime()
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", t)
    print('[{}] {}'.format(time_string, text))


class BaseServerProcess(Process):
    """
    服务端业务进程类,其他业务进程(login/game/map/chat/battle...)继承此类
    """
    def __init__(self, name):
        super(BaseServerProcess, self).__init__()
        self.name = name
        self.socket = socket.socket()
        self.socket.connect(('127.0.0.1', 9093))
        sprint('{}进程连接网关...'.format(self.name))

    def send(self, cmd: str, send_data: dict):
        send_data['cmd'] = cmd
        json_str = json.dumps(send_data)
        json_str_len = len(json_str)
        len_bytes = json_str_len.to_bytes(2, byteorder='big')
        send_bytes = len_bytes + json_str.encode(encoding='utf-8')
        self.socket.sendall(send_bytes)

    def run(self) -> None:
        self.send(self.name, {})  # 向网关注册


class ddict(dict):
    """
    支持用.获取属性值，如d.a=1
    """
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        print('type_:', type(obj))
        # 检查到是bytes类型的数据就转为str类型
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        # 检查到是intc类型的数据就转为str类型
        if isinstance(obj, np.intc):
            return str(round(obj, 2))
        # 检查到是float32类型的数据就转为str类型
        if isinstance(obj, np.float32):
            return str(round(obj, 2))
        # 检查到是datetime.datetime类型的数据就转为str类型
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, socket.socket):
            print('is socket.socket')
            return ''
        return json.JSONEncoder.default(self, obj)


def send(obj, send_data):
    """
    发送网络数据
    obj: 发送对象, 可以是socket, 可以是玩家id
    """
    sk = None
    if type(obj) == socket.socket:
        sk = obj
    elif type(obj) == str:
        sk = SOCKETS[obj]
    else:
        raise 'Unknown socket obj!'

    try:
        sk.send((SOCKET_HEAD + json.dumps(send_data) + SOCKET_HEAD).encode(encoding="utf-8"))
    except:
        pass


def get_players_in_scene(id, include_self=False):
    """
    获取同场景内所有玩家的数据
    :param id: 当前玩家id
    :param include_self: 是否包含这个玩家自己
    """
    players = []
    for pid, p in GL.PLAYERS.items():
        if p['地图'] == GL.PLAYERS[id]['地图']:
            if not include_self and str(p['id']) == str(id):
                continue
            players.append(GL.PLAYERS[pid])
        # print('同地图玩家:', id, include_self, p['id'])
    return players


def formatted_json_to_dict(file):
    json_str = ''
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            json_str += line.replace('\n', '').replace(' ', '')
    return json.loads(json_str)


def get_filenames_in_path(path):
    filenames = []
    if os.path.exists(path):
        for _, _, files in os.walk(path):
            for file in files:
                filenames.append(file)
    return filenames


# 获取所有NPC
def import_npcs():
    files = get_filenames_in_path('./Script/scene/npc')
    with open('Script/scene/npc/npc_importer.py', 'w', encoding='utf-8') as f:
        f.write('from Common import globals as GL\n')
        for file in files:
            if not '__init__' in file and not 'npc_importer' in file and not '.pyc' in file and '.py' in file:
                f.write('from Script.scene.npc.{} import npc\n'.format(file.rstrip('.py')))
                f.write('GL.NPCS.append(npc)\n')
    import Script.scene.npc.npc_importer


def get_df_value(df, df_index, index, field):
    # print('get df value:', df_index, index, field)
    """
    在读取到的dataframe中查找数值
    df: dataframe
    df_index: df的index字段
    index: 要查找的index值
    field: 要查找的field值
    """
    try:
        return df[df[df_index] == index][field].tolist()[0]
    except:
        return 0


def csv2dict(csv_file, index_col=None):
    df = pd.read_csv(csv_file, index_col=index_col)
    rt_dict = df.T.to_dict()
    return rt_dict


def gdv(d, k):
    """
    Get dict value, 获取字典对应键的值
    若存在改键则返回值, 不存在则返回0
    """
    if k not in d:
        return 0
    else:
        return d[k]


def sys_prompt_to_player(pid, text):
    send_data = [S_系统提示, {'内容': text}]
    send(pid, send_data)
