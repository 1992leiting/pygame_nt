import os
import pandas as pd


class Game:
    """
    空类, 存放各种全局变量
    """
    def __init__(self):
        self.director = None
        self.account = ''  # 当前游戏处理的账号
        self.window_layer = None
        self.npcs = {}  # 所有NPC数据,key:npc_id, value:NPC数据

    @property
    def world(self):
        return self.director.get_node('scene/world_scene')

    @property
    def battle_scene(self):
        return self.director.get_node('scene/battle_scene')

    @property
    def hero(self):
        return self.director.get_node('scene/world_scene/hero')

    @property
    def camera(self):
        return self.director.get_node('scene/world_scene/camera')

    @property
    def world_msg_flow(self):
        return self.director.get_node('function_layer/message_area/聊天区背景/信息流文本')

    @property
    def mouse(self):
        return self.director.child('mouse')

    @property
    def sp(self):
        return self.director.child('simple_prompt')

    @property
    def rp(self):
        return self.director.child('rich_prompt')

    @property
    def hero_path(self):
        if self.hero:
            return self.hero.path
        return None


game = Game()


def csv2dict(file_path):
    if not os.path.exists(file_path):
        raise KeyError('CSV file not exist:' + file_path)
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


res_dir = 'F:/pygame/Res/Res/'
if not os.path.exists(res_dir):
    res_dir = 'D:/SynologyDrive/pygame/Res/'
if not os.path.exists(res_dir):
    res_dir = 'D:/pygame/Res/'

rsp_dir = res_dir + 'rsp_new2/'
data_dir = res_dir + 'data/'
map_dir = res_dir + 'mapx/'
font_dir = res_dir + 'font/'
pic_dir = res_dir + 'pic/'
music_dir = res_dir + 'audio/'
sound_dir = res_dir + 'sound/'
winconfig_dir = data_dir + 'WinConfig/'
wpal_dir = res_dir + 'wpal/'

shapes = csv2dict(data_dir + 'normal_shapes.csv')
bshapes = csv2dict(data_dir + 'battle_shapes.csv')
portals = csv2dict(data_dir + 'XA_portals.csv')
colors = csv2dict(data_dir + 'color.csv')
effects = csv2dict(data_dir + 'XA_effects.csv')
head_image = csv2dict(data_dir + 'head_image.csv')
bh_shapes = pd.read_excel(data_dir + 'BH_模型数据.xlsx', index_col='名称').fillna('').T.to_dict()
max_shape_list = pd.read_excel(data_dir + 'max_hash对应表.xlsx', index_col='max_hash').T.to_dict()
BH_NPC_FILE = data_dir + 'BH_NPC数据.xlsx'
BH_MAP_FILE = data_dir + 'BH_地图数据.xlsx'
BH_ITEM_FILE = data_dir + 'BH_物品数据.xlsx'
BH_NPC_DATA = pd.read_excel(BH_NPC_FILE, index_col='地图编号').fillna('').T.to_dict()
BH_MAP_DATA = pd.read_excel(BH_MAP_FILE, index_col='地图编号').fillna('').T.to_dict()
BH_ITEM_DATA = pd.read_excel(BH_ITEM_FILE, index_col='名称').fillna('').T.to_dict()
# ashapes = pd.read_csv(data_dir + 'ashapes.csv', index_col='名称').T.to_dict()

ALPHABET = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'

# 血量类型
HP_DROP = 1  # 掉血
HP_RECOVER = 2  # 加血

# 服务器
SERVER_IP = '127.0.0.1'  # 'ddns.leiting6.cn'
SERVER_PORT = 9093  # 8001

# 默认字体
DEFAULT_FONT = 'simsun.ttf'
SIM_HEI = 'simhei.ttf'
ADOBE_SONG = 'mod_AdobeSong.ttf'

# 阵营
OUR = 1  # 我方
OPPO = 2  # 敌方

# 行走相关
MOVING_SPEED = 2

# 动画相关
MOVING_BACKWARD_DIS = 30  # 战斗中击退的距离
EFFECT_FPS = 10  # 默认法术特效的FPS

# 鼠标动作序号
MOUSE_LEFT_DOWN = 0
MOUSE_RIGHT_DOWN = 1
MOUSE_LEFT_RELEASE = 2
MOUSE_RIGHT_RELEASE = 3

# 鼠标事件处理标记
PASS = 0  # 捕获不清空事件
STOP = 1  # 捕获并清空事件
IGNORE = 2  # 忽略事件

# 场景代号
WORLD_SCENE = 0
BATTLE_SCENE= 1

MY_COLOR = {
    # key: 颜色代号, 富文本中#号后面跟的字母
    # val: color.csv文件中的颜色描述
    'R': '红',
    'G': '酸橙',
    'B': '蓝',
    'Y': '黄',
    'K': '黑',
    'W': '白',
    'P': '紫红',
    'S': '洋红',  # 接近品红
}

# 梦幻表情包子
MY_EMOJI = [1295847816,1853525647,1076954610,3552721044,3990239921,3366615112,2782337201,3771134163,1462708813,2715893287,3002376600,3991654351,993860032,2666294756,454787878,1382010105,2912848813,3919700593,477926852,352380776,811687356,915719759,4249060934,1336751228,1950021903,2235513801,3594739784,1960900090,2382390242,1537855326,3907030953,2290431679,3202252097,4033571742,1492820992,655187057,2901001332,3190903022,298183232,1945354141,3436623848,1724964988,2592865169,3393696884,1494002331,1310769894,1152800681,2542768010,1378600591,2829693277,3846038890,3901444948,68667698,3331959614,432707334,4241851683,3448703702,2542506275,241536076,314448958,2242677963,1887092560,1489631920,2860202818,4076591726,4232189420,3498505860,4241140149,3858705890,2271353759,3452523393,963399171,2959831232,2917226350,4215743335,3987108486,365569753,3701218951,3044567112,3265766525,2129343522,2401287726,2716317030,292723042,4014574629,4183102172,4115700508,2139528734,276624883,4099788650,2578443618,3367759523,576638850,3586214754,2830927389,1915332364,1341579386,3743372972,1217313750,1208397371,156713767,2057251015,3084935361,1485268859,470535714,2868631088,3835251562,2896374671,3982186902,1708428735,2448085336,1354708809,943667221,1146784672,3592760724,611393967,1688780051,2042812914,1466206851,770780432,3612578974,0x0F7FA3E5,0x1C9419F8,0x1D3F0301,0x1C9419F8,0x2C3FC5BB,0x2DA6CCAF,0x3A7BCB44,0x3FB960DE,0x4F692A7B,0x4FD80C52,0x6E92200B,0x7A482A89,0x8D177ED8,0x8D956A19,0x9EEFD716,0x42A7366B,0x047A251B,0x047D0BD0,0x50D0D23E,0x65FBF6CC,0x71E5FA65,0x8D177ED8,0x8D956A19,0x640A80F4]

# 频道表情
CHL_EMOJI = {
    'xt': 1131417125,
    'sj': 0x1B1DCE56,
    'dq': 0x65C5B7EE,
    'sl': 0xF9ADC3DA,
    'gm': 0xE8897A81,
    'cw': 0xCD23D726,
    'bp': 0xAD9D6490,
    'dw': 0xF9858C95
}

# 频道代码
CHL_CODE = dict(
    系统='#xt',
    世界='#sj',
    当前='#dq',
    私聊='#sl',
    GM='#gm',
    传闻='#cw',
    帮派='#bq',
    队伍='#dw'
)

# nt manager QT UI相关
COL_NODE = 0
COL_TYPE = 1
COL_NAME = 2
COL_UUID = 3
NODE_LIST = [
    'Node', 'Animation', 'Animation8D', 'Button', 'Director', 'ImageRect', 'Label', 'ProgressBar', 'RichText',
    'TextEdit', 'LineEdit', 'Camera', 'BasicCharacter', 'Character', 'NPC', 'BattleUnit', 'Emoji', 'HpEffect',
    'BuffEffect', 'MagicEffect', 'FullScreenEffect', 'MapMask', 'Mouse', 'Portal', 'World'
]

# Prompt相关
GAME_PROMPT = 0  # 系统提示风格
CHAR_SPEECH = 1  # 玩家发言风格
FLOATING_PROMPT = 2  # 悬浮提示
PROMPT_MARGIN_X = 5  # 系统提示文字距离边框的距离
PROMPT_MARGIN_Y = 5
CHAR_SPEECH_PROMPT_WIDTH = 106
PROMPT_WIDTH = {
    CHAR_SPEECH: CHAR_SPEECH_PROMPT_WIDTH,
    GAME_PROMPT: 300,
    FLOATING_PROMPT: 10
}
PROMPT_Y_SPACE = {
    CHAR_SPEECH: 4,
    GAME_PROMPT: 7,
}  # 提示之间的间距
PROMPT_TIMEOUT = {
    CHAR_SPEECH: 10,
    GAME_PROMPT: 5
}  # 超时消失的时间

HERO_MODELS = ["飞燕女", "英女侠", "逍遥生", "剑侠客", "狐美人", "骨精灵", "巨魔王", "虎头怪", "舞天姬", "玄彩娥", "神天兵", "龙太子"]


# 小地图相关
SMAP_NPC_COLOR = dict(
    全部='深青',
    普通='白',
    商业='金',
    特殊='橙红',
    传送='酸橙',
    任务='深天蓝',
    出口='紫'
)


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