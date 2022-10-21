import os


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

rsp_dir = res_dir + 'rsp/'
data_dir = res_dir + 'data/'
map_dir = res_dir + 'mapx/'
font_dir = res_dir + 'font/'
pic_dir = res_dir + 'pic/'
music_dir = res_dir + 'audio/'
sound_dir = res_dir + 'sound/'

shapes = csv2dict(data_dir + 'normal_shapes.csv')
bshapes = csv2dict(data_dir + 'battle_shapes.csv')
portals = csv2dict(data_dir + 'XA_portals.csv')
colors = csv2dict(data_dir + 'color.csv')
effects = csv2dict(data_dir + 'XA_effects.csv')
# ashapes = pd.read_csv(data_dir + 'ashapes.csv', index_col='名称').T.to_dict()

# 血量类型
HP_DROP = 1  # 掉血
HP_RECOVER = 2  # 加血

# 服务器
SERVER_IP = 'ddns.leiting6.cn'
SERVER_PORT = 8001

# 默认字体
DEFAULT_FONT = 'simsun.ttf'

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
    'bq': 0xAD9D6490,
    'dw': 0xF9858C95
}

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
