import os
import pandas as pd


class Server:
    def __init__(self):
        self.players = {}  # 所有玩家信息
        self.tasks = {}  # 所有人物数据
        self.npc_objects = {}  # 所有的NPC数据


server = Server()


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
BATTLE_SERVER_REGISTER_CMD = 'battle-server-U84D7835JINGR874HTGK3934J'  # 每次battle server进程向gateway注册时的cmd
DATA_PATH = 'data/'
ACCOUNT_SUMMARY_PATH = DATA_PATH + 'account_summary.json'

PORTALS = csv2dict('database/XA_portals.csv')  # 地图传送点
NPCS = csv2dict('database/npc.csv')

CONFIG_DATA_PATH = 'D:/SynologyDrive/pygame/Res/data/'
if not os.path.exists(CONFIG_DATA_PATH):
    CONFIG_DATA_PATH = r'F:\pygame\Res\Res\data/'
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

empty_20 = {'0': None, '1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None,
            '8': None, '9': None, '10': None, '11': None, '12': None, '13': None, '14': None,
            '15': None, '16': None, '17': None, '18': None, '19': None}


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
