import os
import pandas as pd


def csv2dict(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError('CSV file not exist: ' + file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        dic = {}
        row = f.readline()
        _heads = row.split(',')  # csv头为第一行
        heads = []
        for head in _heads:
            heads.append(head.strip().strip('\ufeff'))
        for row in f.readlines():
            row_items = row.split(',')
            key = row_items[0]
            dic[key] = {}
            for i, value in enumerate(row_items):
                if i == 0:
                    continue
                head = heads[i]
                dic[key][head] = value.strip()
    return dic


def parse_cell(data: str):
    """
    解析excel中单元格的数据, {...,...,...}
    :param data:
    :return:
    """
    rt = []
    if not data:
        return rt
    data = data.lstrip('{').rstrip('}').split(',')
    for d in data:
        if d.isdigit():
            rt.append(int(d))
        else:
            rt.append(d)
    return rt


def find_npc_map(npc_id):
    """
    找到npc在哪个地图中
    :param npc_id:
    :return:
    """
    npc_id = int(npc_id)
    for map_id, data in BH_MAP_DATA.items():
        npcs = parse_cell(data['NPC'])
        if npc_id in npcs:
            return map_id
    return None


REDIS_AUTO_SAVE_INTERVAL = 60
GATEWAY_SERVER = ('127.0.0.1', 9093)
GAME_SERVER_REGISTER_CMD = 'game-server-U84JFNF9845N329FJRM44IF84H'  # 每次game server进程向gateway注册时的cmd
DATA_PATH = 'data/'
ACCOUNT_SUMMARY_PATH = DATA_PATH + 'account_summary.json'

PORTALS = csv2dict('database/XA_portals.csv')  # 地图传送点
NPCS = csv2dict('database/npc.csv')

CONFIG_DATA_PATH = 'D:/SynologyDrive/pygame/Res/data/'
BH_NPC_FILE = CONFIG_DATA_PATH + 'BH_NPC数据.xlsx'
BH_MAP_FILE = CONFIG_DATA_PATH + 'BH_地图数据.xlsx'
BH_NPC_DATA = pd.read_excel(BH_NPC_FILE, index_col='地图编号').fillna('').T.to_dict()
BH_MAP_DATA = pd.read_excel(BH_MAP_FILE, index_col='地图编号').fillna('').T.to_dict()
for npc_id, data in BH_NPC_DATA.items():
    map_id = find_npc_map(npc_id)
    BH_NPC_DATA[npc_id]['地图'] = map_id

CHAR = 'char'
ITEM = 'item'
ITEMW = 'item_warehouse'
PET = 'pet'
PETW = 'pet_warehouse'
