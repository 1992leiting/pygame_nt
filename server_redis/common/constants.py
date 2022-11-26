import os


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


REDIS_AUTO_SAVE_INTERVAL = 60
GATEWAY_SERVER = ('127.0.0.1', 9093)
GAME_SERVER_REGISTER_CMD = 'game-server-U84JFNF9845N329FJRM44IF84H'  # 每次game server进程向gateway注册时的cmd
DATA_PATH = 'data/'
ACCOUNT_SUMMARY_PATH = DATA_PATH + 'account_summary.json'

PORTALS = csv2dict('database/XA_portals.csv')  # 地图传送点
NPCS = csv2dict('database/npc.csv')

CHAR = 'char'
ITEM = 'item'
ITEMW = 'item_warehouse'
PET = 'pet'
PETW = 'pet_warehouse'
