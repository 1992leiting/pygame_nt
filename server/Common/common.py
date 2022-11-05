from Common import constants as GL
from Common.socket_id import *
import numpy as np
import datetime
import socket
import json
import os
import pickle
import time
import pandas as pd


# 游戏参数
SOCKET_HEAD = '#$#$#'
SOCKET_TAIL = '$#$#$'
GAME_辅助技能 = ["强身术", "冥想", "强壮", "暗器技巧", "中药医理", "烹饪技巧", "打造技巧", "裁缝技巧", "炼金术", "养生之道", "健身术", "巧匠之术"]

# 人物升级经验
CHAR_LEVEL_EXP_REQ = [40, 110, 237, 450, 779, 1252, 1898, 2745, 3822, 5159, 6784, 8726, 11013, 13674, 16739, 20236,
                      24194, 28641, 33606, 39119, 45208, 51902, 55229, 67218, 75899, 85300, 95450, 106377, 118110,
                      130679, 144112, 158438, 173685, 189882, 207059, 225244, 244466, 264753, 286134, 308639, 332296,
                      357134, 383181, 410466, 439019, 468868, 500042, 532569, 566478, 601799, 638560, 676790, 716517,
                      757770, 800579, 844972, 890978, 938625, 987942, 1038959, 1091704, 1146206, 1202493, 1260594,
                      1320539, 1382356, 1446074, 1511721, 1579326, 1648919, 1720528, 1794182, 1869909, 1947738, 2027699,
                      2109820, 2194130, 2280657, 2369431, 2460479, 2553832, 2649518, 2747565, 2848003, 2950859, 3056164,
                      3163946, 3274233, 3387055, 3502439, 3620416, 3741014, 3864261, 3990187, 4118819, 4250188, 4384322,
                      4521249, 4660999, 4803599, 4998571, 5199419, 5406260, 5619213, 5838397, 6063933, 6295941, 6534544,
                      6779867, 7032035, 7291172, 7557407, 7830869, 8111686, 8399990, 8695912, 8999586, 9311145, 9630726,
                      9958463, 10294496, 10638964, 10992005, 11353761, 11724374, 12103988, 12492748, 12890799, 13298287,
                      13715362, 14142172, 14578867, 15025600, 15482522, 15949788, 16427552, 16915970, 17415202,
                      17925402, 18446732, 18979354, 19523428, 20079116, 20646584, 21225998, 43635044, 44842648,
                      46075148, 47332886, 48616200, 74888148,
                      76891401, 78934581, 81018219, 83142835, 85308969, 87977421, 89767944, 92061870, 146148764,
                      150094780, 154147340, 158309318,
                      162583669, 166973428, 171481711, 176111717, 180866734, 185780135, 240602904, 533679362, 819407100,
                      1118169947, 1430306664,
                      1756161225, 2096082853]


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
    global SOCKET_HEAD, SOCKET_TAIL
    if type(obj) == socket.socket:
        sk = obj
    elif type(obj) == str:
        sk = GL.SOCKETS[obj]
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
        f.write('from Script.common import globals as GL\n')
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
