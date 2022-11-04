from Script.common import constants as GL
from Script.common.common import *
from Script.scene.scene_handler import *
import os
import time


# 气血/气血上限/最大气血
# 魔法/最大魔法
initial_player_data = dict(节日礼物=0, id='my1001', 连接ip=0, 等级=0, 名称="", 性别=0, 模型="", 种族="", 称谓={}, 当前称谓="", 帮派="无帮派",
                           门派="无门派",
                           人气=600, 门贡=0, 帮贡=0, 气血=0, 魔法=0, 愤怒=0, 活力=0, 体力=0, 命中=0, 伤害=0, 防御=0, 速度=0, 躲避=0, 灵力=0, 法伤属性=0,
                           法防属性=0, 体质=0, 魔力=0, 力量=0, 耐力=0, 敏捷=0, 总财富=0, 潜力=5, 地图=1501, mx=20, my=20,
                           修炼={'攻击修炼': [0, 0, 9], '法术修炼': [0, 0, 9], '防御修炼': [0, 0, 9], '抗法修炼': [0, 0, 9],
                               '猎术修炼': [0, 0, 9], '当前': "攻击修炼"},
                           bb修炼={'攻击控制力': [0, 0, 9], '法术控制力': [0, 0, 9], '防御控制力': [0, 0, 9], '抗法控制力': [0, 0, 9],
                                 '当前': "攻击控制力"}, 最大体力=100, 最大活力=100, 最大气血=0, 最大魔法=0, 当前经验=0, 最大经验=0, 宝宝列表={}, 子女列表={},
                           参战宝宝={}, 可选门派={}, 使用装备=1, 装备={}, 灵饰={}, 锦衣={}, 法宝={}, 师门技能={}, 人物技能={}, 特殊技能={},
                           辅助技能=dict(强身术=0, 冥想=0, 强壮=0, 暗器技巧=0, 中药医理=0, 烹饪技巧=0, 打造技巧=0, 裁缝技巧=0, 炼金术=0, 养生之道=0, 健身术=0,
                                     巧匠之术=0),
                           战斗技能={}, 快捷技能={}, 染色方案=0, 染色组={}, 技能等级=[0, 0, 0, 0],
                           装备属性=dict(气血=0, 魔法=0, 命中=0, 伤害=0, 防御=0, 速度=0, 躲避=0, 灵力=0, 体质=0, 魔力=0, 力量=0, 耐力=0, 敏捷=0,
                                     月饼=0),
                           技能属性=dict(气血=0, 魔法=0, 命中=0, 伤害=0, 防御=0, 速度=0, 躲避=0, 灵力=0, 体质=0, 魔力=0, 力量=0, 耐力=0, 敏捷=0),
                           乾元丹=0, 附加乾元丹=0, 剩余乾元丹=0, 可换乾元丹=0,
                           奇经八脉={}, 人物状态={}, 变身={}, 默认技能=False, 可持有武器=None,
                           自动=None, 在线时间=0, 剧情点=0, 官职点=0, 官职次数=0, 师门次数=0, 套装={}, 法宝佩戴={}, 自动遇怪=False,
                           江湖次数=0, 江湖取消=0, 助战=0, 新手奖励={}, 好友数据={'好友': [], '临时': [], '最近': [], '黑名单': []}, 新手银子={},
                           新手礼包={}, 剧情={}, 坐骑列表={}, 坐骑=None, 穿戴锦衣=None, 穿戴足印=None, 穿戴足迹=None, 穿戴装饰=None, 洗点次数=0,
                           战斗场次=0,
                           死亡次数=0, 比武积分=0, 孩子数量=0, 赏金任务次数=0, 成就={}, 现金=0, 存银=0, 储备金=0, 气血上限=0,
                           道具={'0': None, '1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None,
                               '8': None, '9': None, '10': None, '11': None, '12': None, '13': None, '14': None,
                               '15': None, '16': None, '17': None, '18': None, '19': None},
                           行囊={'0': None, '1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None,
                               '8': None, '9': None, '10': None, '11': None, '12': None, '13': None, '14': None,
                               '15': None, '16': None, '17': None, '18': None, '19': None})

initial_model_attr = dict(
    飞燕女=dict(模型="飞燕女", ID=1, 染色方案=3, 性别="女", 种族="人", 门派=["大唐官府", "女儿村", "方寸山", "神木林"], 武器=["双剑", "环圈"]),
    英女侠=dict(模型="英女侠", ID=2, 染色方案=4, 性别="女", 种族="人", 门派=["大唐官府", "女儿村", "方寸山", "神木林"], 武器=["双剑", "鞭"]),
    巫蛮儿=dict(模型="巫蛮儿", ID=3, 染色方案=1, 性别="女", 种族="人", 门派=["大唐官府", "女儿村", "方寸山", "神木林"], 武器=["宝珠", "法杖"]),
    逍遥生=dict(模型="逍遥生", ID=4, 染色方案=1, 性别="男", 种族="人", 门派=["大唐官府", "化生寺", "方寸山", "神木林"], 武器=["扇", "剑"]),
    剑侠客=dict(模型="剑侠客", ID=5, 染色方案=2, 性别="男", 种族="人", 门派=["大唐官府", "化生寺", "方寸山", "神木林"], 武器=["刀", "剑"]),
    狐美人=dict(模型="狐美人", ID=6, 染色方案=7, 性别="女", 种族="魔", 门派=["盘丝洞", "阴曹地府", "魔王寨", "无底洞"], 武器=["爪刺", "鞭"]),
    骨精灵=dict(模型="骨精灵", ID=7, 染色方案=8, 性别="女", 种族="魔", 门派=["盘丝洞", "阴曹地府", "魔王寨", "无底洞"], 武器=["魔棒", "爪刺"]),
    杀破狼=dict(模型="杀破狼", ID=8, 染色方案=1, 性别="男", 种族="魔", 门派=["狮驼岭", "阴曹地府", "魔王寨", "无底洞"], 武器=["宝珠", "弓弩"]),
    巨魔王=dict(模型="巨魔王", ID=9, 染色方案=5, 性别="男", 种族="魔", 门派=["狮驼岭", "阴曹地府", "魔王寨", "无底洞"], 武器=["刀", "斧钺"]),
    虎头怪=dict(模型="虎头怪", ID=10, 染色方案=6, 性别="男", 种族="魔", 门派=["狮驼岭", "阴曹地府", "魔王寨", "无底洞"], 武器=["斧钺", "锤子"]),
    舞天姬=dict(模型="舞天姬", ID=11, 染色方案=11, 性别="女", 种族="仙", 门派=["天宫", "普陀山", "龙宫", "凌波城"], 武器=["飘带", "环圈"]),
    玄彩娥=dict(模型="玄彩娥", ID=12, 染色方案=12, 性别="女", 种族="仙", 门派=["天宫", "普陀山", "龙宫", "凌波城"], 武器=["飘带", "魔棒"]),
    羽灵神=dict(模型="羽灵神", ID=13, 染色方案=1, 性别="男", 种族="仙", 门派=["天宫", "普陀山", "龙宫", "凌波城"], 武器=["法杖", "弓弩"]),
    神天兵=dict(模型="神天兵", ID=14, 染色方案=9, 性别="男", 种族="仙", 门派=["天宫", "五庄观", "龙宫", "凌波城"], 武器=["锤", "枪矛"]),
    龙太子=dict(模型="龙太子", ID=15, 染色方案=10, 性别="男", 种族="仙", 门派=["天宫", "五庄观", "龙宫", "凌波城"], 武器=["扇", "枪矛"]),
    桃夭夭=dict(模型="桃夭夭", ID=16, 染色方案=1, 性别="女", 种族="仙", 门派=["天宫", "普陀山", "龙宫", "凌波城"], 武器=["灯笼"]),
    偃无师=dict(模型="偃无师", ID=17, 染色方案=1, 性别="男", 种族="人", 门派=["大唐官府", "化生寺", "方寸山", "神木林"], 武器=["剑", "巨剑"]),
    鬼潇潇=dict(模型="鬼潇潇", ID=18, 染色方案=2, 性别="女", 种族="魔", 门派=["盘丝洞", "阴曹地府", "魔王寨", "无底洞"], 武器=["爪刺", "伞"])
)

# 各种族的初始点数分配
initial_race_points = dict(
    人=[10, 10, 10, 10, 10],
    魔=[12, 11, 11, 8, 8],
    仙=[12, 5, 11, 12, 10],
)


def send_hero_data(id):
    sk = GL.SOCKETS[id]
    send_data = [S_发送主角信息, {'主角': GL.PLAYERS[id]}]
    send(sk, send_data)


def update_player_xy(data):
    """
    刷新玩家的地图坐标mx, my
    """
    pid = data['id']
    if pid in GL.PLAYERS:
        mx, my = data['mx'], data['my']
        GL.PLAYERS[pid]['mx'], GL.PLAYERS[pid]['my'] = mx, my

        # 队伍跟随, 队员跟随
        dis = 1  # 队员和队长的距离为1, 队员之间距离为1
        for cap, team in GL.TEAMS.items():
            if pid in team:
                pos = team.index(pid)  # 队伍位置, 0为队长, 1-4为队员
                if pos == 0:  # 队长不跟随
                    return
                elif pos > 1:
                    dis = 1  # 设置队员之间的距离

                follow_id = team[pos - 1]
                follow_x, follow_y = GL.PLAYERS[follow_id]['mx'], GL.PLAYERS[follow_id]['my']
                if abs(mx - follow_x) <= dis or abs(my - follow_y) <= dis:
                    # 如果距离很近则停止移动
                    update_player_path({'id': pid, '路径': []})
                else:
                    # 如果距离超过设定值则触发寻路
                    send_data = [S_人物触发寻路, {'mx': follow_x, 'my': follow_y}]
                    send(pid, send_data)


def update_player_path(data):
    """
    玩家寻路时, 把路径发给同场景其他玩家
    """
    id = data['id']
    path = data['路径']
    players = get_players_in_scene(id)
    for p in players:
        pid = p['id']
        send_data = [S_发送路径, {'id': id, '路径': path}]
        sk = GL.SOCKETS[pid]
        send(sk, send_data)


def player_log_in(pid, account, sk, client_address):
    player_data = formatted_json_to_dict('./data/' + account + '/' + pid + '/角色数据.json')
    GL.PLAYERS[pid] = player_data
    GL.PLAYERS[pid]['ip'] = client_address[0]
    GL.PLAYERS[pid]['port'] = client_address[1]
    GL.PLAYERS[pid]['account'] = account
    GL.PLAYERS[pid]['传送完成'] = True
    GL.PLAYERS[pid]['队长'] = False
    GL.PLAYERS[pid]['战斗中'] = False
    GL.PLAYERS[pid]['队伍'] = None
    GL.SOCKETS[pid] = sk

    item_file = './data/' + account + '/' + pid + '/物品数据.json'
    if not os.path.exists(item_file):
        GL.ITEMS[pid] = {}
    else:
        GL.ITEMS[pid] = formatted_json_to_dict(item_file)  # csv2dict(item_file, index_col='id')
    refresh_play_attr(pid)
    send_hero_data(pid)
    player_enter_scene(pid)


def player_log_out(pid, err_text=None, err_tp=None):
    remove_player_from_scene(pid)  # 通知其他玩家从场景中删除该玩家
    try:
        # print('玩家退出:', GL.PLAYERS, GL.SOCKETS)
        save_player_data(pid)  # 保存数据
        leave_team(pid)  # 离开队伍
        sk = GL.SOCKETS[pid]
        if err_text is not None and err_tp is not None:
            send_data = [S_系统错误, {'类型': err_tp, '内容': err_text}]
            send(sk, send_data)
        GL.PLAYERS.pop(pid)
        GL.SOCKETS.pop(pid)
        sk.close()
    except BaseException as e:
        raise e
        # print('__玩家退出错误:', str(e))


def save_player_data(pid):
    if pid in GL.PLAYERS:
        account = GL.PLAYERS[pid]['account']
        with open('./data/' + account + '/' + pid + '/角色数据tmp.json', 'w', encoding='utf-8') as f:
            json.dump(GL.PLAYERS[pid], f, cls=MyEncoder, ensure_ascii=False)
        os.remove('./data/' + account + '/' + pid + '/角色数据.json')
        os.rename('./data/' + account + '/' + pid + '/角色数据tmp.json',
                  './data/' + account + '/' + pid + '/角色数据.json')


def be_captain(pid):
    GL.PLAYERS[pid]['队长'] = True
    GL.TEAMS[pid] = [pid]
    print('成为队长', pid, GL.TEAMS)
    update_player_data_in_scene(pid, pid, {'队长': True, '队伍': pid})


def apply_for_team(pid, target_id):
    """
    申请组队
    pid: 申请人id
    target_id: 对象玩家id
    """
    # 如果对方是队长, 则加入队伍
    if target_id in GL.TEAMS:
        GL.TEAMS[target_id].append(pid)
        GL.PLAYERS[pid]['队伍'] = target_id
        # 加入队伍后跑向队长坐标处
        sk = GL.SOCKETS[pid]
        # target_xy = (GL.PLAYERS[target_id]['mx'], GL.PLAYERS[target_id]['my'])
        send_data = [S_加入队伍, {'目标id': target_id}]
        print('申请加入队伍:', pid, target_id, GL.TEAMS, send_data)
        send(sk, send_data)
        send_hero_data(pid)


def leave_team(pid):
    _teams = GL.TEAMS.copy()
    for cap, team in _teams.items():  # TODO: 战斗中待处理
        # 是队长则删除队伍信息
        if cap == pid:
            print('队长离队:', pid)
            for mem_id in team:
                update_player_data_in_scene(mem_id, mem_id, {'队长': False, '队伍': None})
            del GL.TEAMS[pid]
        # 是队员则离开队伍
        elif pid in team:
            print('队员离队:', pid)
            GL.TEAMS[cap].remove(pid)
            update_player_data_in_scene(pid, pid, {'队长': False, '队伍': None})


def create_player(account, pid, name, model):
    print('创建角色:', account, pid, name, model, os.path.exists('./data/' + account + '/' + pid))
    if not os.path.exists('./data/' + account + '/' + pid):
        os.makedirs('./data/' + account + '/' + pid)
        player_data = initial_player_data.copy()
        player_data['id'] = pid
        player_data['名称'] = name
        player_data['模型'] = model

        player_data['性别'] = initial_model_attr[model]['性别']
        # player_data['ip'] = ip
        player_data['模型'] = initial_model_attr[model]['模型']
        player_data['存银'] = 0
        player_data['助战'] = 0
        player_data['熟练'] = 0
        player_data['阴德'] = 0
        player_data['节日礼物'] = 0
        player_data['坐骑'] = []
        player_data['锦衣'] = []
        player_data['穿戴锦衣'] = None
        player_data['穿戴足印'] = None
        player_data['穿戴足迹'] = None
        player_data['穿戴装饰'] = None
        player_data['快捷技能'] = []
        player_data['阵法'] = dict(普通=1)
        player_data['出生日期'] = int(time.time())
        player_data['造型'] = initial_model_attr[model]['模型']
        player_data['地图'] = 1501
        player_data['mx'] = 37
        player_data['my'] = 12
        player_data['种族'] = initial_model_attr[model]['种族']
        player_data['可选门派'] = initial_model_attr[model]['门派']
        player_data['武器数据'] = dict(名称="", 子类="", 等级=0)
        player_data['染色组'] = None
        player_data['奇经八脉'] = {}
        player_data['染色方案'] = initial_model_attr[model]['染色方案']
        player_data['任务'] = {}
        player_data['新手礼包'] = {}
        player_data['可持有武器'] = initial_model_attr[model]['武器']
        player_data['主线'] = 0
        player_data['支线'] = 0
        player_data['道具仓库'] = {'1': [], '2': [], '3': []}
        player_data['召唤兽仓库'] = {'1': []}
        player_data['宠物'] = dict(模型="生肖猪", 名称="生肖猪", 等级=1, 最大等级=120, 耐力=5, 最大耐力=5, 经验=1, 最大经验=10, 领养次数=0)
        player_data['体质'] = initial_race_points[player_data['种族']][0]
        player_data['魔力'] = initial_race_points[player_data['种族']][1]
        player_data['力量'] = initial_race_points[player_data['种族']][2]
        player_data['耐力'] = initial_race_points[player_data['种族']][3]
        player_data['敏捷'] = initial_race_points[player_data['种族']][4]
        player_data['剧情点'] = 0
        player_data['剧情'] = {}
        player_data['坐骑列表'] = []
        player_data['新账号'] = True

        json.dump(player_data, open('./data/' + account + '/' + pid + '/' + '角色数据.json', 'w', encoding='utf-8'),
                  ensure_ascii=False)
        json.dump({}, open('./data/' + account + '/' + pid + '/' + '物品数据.json', 'w', encoding='utf-8'),
                  ensure_ascii=False)
        json.dump({}, open('./data/' + account + '/' + pid + '/' + '召唤兽数据.json', 'w', encoding='utf-8'),
                  ensure_ascii=False)
        if not os.path.exists('./data/' + account + '/' + '账号数据.json'):
            json.dump(dict(密码=123456), open('./data/' + account + '/' + '账号数据.json', 'w', encoding='utf-8'),
                      ensure_ascii=False)


def get_5d_attr(pid):
    player_data = GL.PLAYERS[pid]
    体质 = player_data['体质']
    魔力 = player_data['魔力']
    力量 = player_data['力量']
    耐力 = player_data['耐力']
    敏捷 = player_data['敏捷']
    race = player_data['种族']

    if race == '人':
        attr = dict(
            命中=int(力量 * 2 + 30),
            伤害=int(力量 * 0.67 + 39),
            防御=int(耐力 * 1.5),
            速度=int(敏捷),
            灵力=int(体质 * 0.3 + 魔力 * 0.7 + 耐力 * 0.2 + 力量 * 0.4),
            躲避=int(敏捷 + 10),
            气血=int(体质 * 5 + 100),
            法力=int(魔力 * 3 + 80)
        )
    elif race == '魔':
        attr = dict(
            命中=int(力量 * 2.3 + 29),
            伤害=int(力量 * 0.77 + 39),
            防御=int(耐力 * 214 / 153),
            速度=int(敏捷),
            灵力=int(体质 * 0.3 + 魔力 * 0.7 + 耐力 * 0.2 + 力量 * 0.4 - 0.3),
            躲避=int(敏捷 + 10),
            气血=int(体质 * 6 + 100),
            法力=int(魔力 * 2.5 + 80),
        )
    else:
        attr = dict(
            命中=int(力量 * 1.7 + 30),
            伤害=int(力量 * 0.57 + 39),
            防御=int(耐力 * 1.6),
            速度=int(敏捷),
            灵力=int(体质 * 0.3 + 魔力 * 0.7 + 耐力 * 0.2 + 力量 * 0.4 - 0.3),
            躲避=int(敏捷 + 10),
            气血=int(体质 * 4.5 + 100),
            法力=int(魔力 * 3.5 + 80),
        )
    return attr


def refresh_play_attr(pid, recover=None, send_data=False):
    """
    更新人物属性
    pid: 玩家id
    recover: 是否恢复 0:气血/1:魔法/2:都恢复
    send_data: 是否发送数据到客户端
    """
    if pid not in GL.PLAYERS:
        return
    player_data = GL.PLAYERS[pid]
    # 钱数额取整
    player_data['现金'] = int(player_data['现金'])
    player_data['存银'] = int(player_data['存银'])
    player_data['储备金'] = int(player_data['储备金'])

    # 五维基础属性
    attr_5d = get_5d_attr(pid)

    # 五维属性
    player_data['命中'] = attr_5d['命中'] + player_data['装备属性']['命中'] + player_data['技能属性']['命中']
    player_data['伤害'] = attr_5d['伤害'] + player_data['装备属性']['伤害'] + player_data['技能属性']['伤害']
    player_data['防御'] = attr_5d['防御'] + player_data['装备属性']['防御'] + player_data['技能属性']['防御']
    player_data['速度'] = attr_5d['速度'] + player_data['装备属性']['速度'] + player_data['技能属性']['速度']
    player_data['灵力'] = attr_5d['灵力'] + player_data['装备属性']['灵力'] + player_data['技能属性']['灵力']
    player_data['躲避'] = attr_5d['命中'] + player_data['装备属性']['躲避'] + player_data['技能属性']['躲避']
    player_data['最大气血'] = attr_5d['气血'] + player_data['装备属性']['气血'] + player_data['技能属性']['气血'] + player_data['辅助技能'][
        '强壮'] * 4
    player_data['最大魔法'] = attr_5d['法力'] + player_data['装备属性']['魔法'] + player_data['技能属性']['魔法']
    player_data['法伤属性'] = int(player_data['灵力'] + gdv(player_data, '附加法术伤害') + gdv(player_data, '法术伤害') + gdv(player_data['装备属性'], '伤害')/4)
    player_data['法防属性'] = int(player_data['灵力'] + gdv(player_data, '法术防御'))

    if recover is not None:
        if recover == 0 or recover == 2:
            player_data['气血上限'] = player_data['最大气血']
            player_data['气血'] = player_data['最大气血']
        if recover == 1 or recover == 2:
            player_data['魔法'] = player_data['最大魔法']

    if send_data:
        send_hero_data(pid)


def player_人物确认加点(pid, points: list):
    player_data = GL.PLAYERS[pid]
    sum_points = sum(points)
    if sum_points <= player_data['潜力']:
        player_data['潜力'] -= sum_points
    player_data['体质'] += points[0]
    player_data['魔力'] += points[1]
    player_data['力量'] += points[2]
    player_data['耐力'] += points[3]
    player_data['敏捷'] += points[4]

    if points[0] > 0:
        refresh_play_attr(pid, recover=0)
    if points[1] > 0:
        refresh_play_attr(pid, recover=1)
    refresh_play_attr(pid, send_data=True)


def player_level_up(pid):
    """
    玩家升级处理
    """
    player_data = GL.PLAYERS[pid]
    lv = player_data['等级']
    if player_data['当前经验'] >= CHAR_LEVEL_EXP_REQ[lv]:
        player_data['当前经验'] -= CHAR_LEVEL_EXP_REQ[lv]
        player_data['等级'] += 1
        player_data['体质'] += 1
        player_data['魔力'] += 1
        player_data['力量'] += 1
        player_data['耐力'] += 1
        player_data['敏捷'] += 1
        player_data['潜力'] += 5
        player_data['最大活力'] += 10
        player_data['最大体力'] += 10
        refresh_play_attr(pid, send_data=True, recover=2)
        send_player_effect(pid, '升级')
    else:
        sys_prompt_to_player(pid, '你没有那么多经验')


def send_player_effect(pid, effect):
    """
    发送人物场景特效, 位置跟随人物, 比如升级
    """
    players = get_players_in_scene(pid, include_self=True)
    for p in players:
        send_data = [S_人物场地特效, {'id': pid, '特效': effect}]
        send(p['id'], send_data)


