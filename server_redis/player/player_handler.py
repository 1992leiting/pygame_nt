from common.common import *
from common.constants import *
from common.socket_id import *
from common.server_process import server
import os


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

initial_player_data = dict(节日礼物=0, id=0, 连接ip=0, 等级=0, 名称="", 性别=0, 模型="", 种族="", 称谓={}, 当前称谓="", 帮派="无帮派",
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
                           奇经八脉={}, 人物状态={}, 变身={}, 默认技能=False, 可持有武器=[], 可加入门派=[],
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
initial_item_data = dict(道具={}, 行囊={})
initial_itemwarehouse_data = dict(主仓库={}, 房屋仓库={})
initial_pet_data = dict()
initial_petwarehouse_data = dict(主仓库={}, 房屋仓库={})


def create_player(account, name, model):
    """
    创建角色先创建文件再读入redis
    :param account:
    :param name:
    :param model:
    :return:
    """
    # 通过遍历account summary确认pid
    pid = 0
    acc_sm = redis_get_data(server.redis_conn, 'account_summary')
    for i in range(10001, 99999):
        if str(i) not in acc_sm:
            pid = i
            break
    if not pid:
        sprint('创建角色时生成pid错误:{} {} {} {}'.format(account, pid, name, model), 'error')
        return
    if name in acc_sm.values():
        send(gateway_socket.cur_socket, S_系统提示, dict(内容='角色名称已存在'))
        sprint('角色名称已存在:{} {} {} {}'.format(account, pid, name, model))
        return

    account_path = os.path.join(DATA_PATH, str(account))
    pid_path = os.path.join(account_path, str(pid))
    if not os.path.exists(account_path):
        sprint('账号不存在,无法创建角色:{} {} {} {}'.format(account, pid, name, model), 'warning')
        return
    if os.path.exists(pid_path):
        sprint('角色id已存在,无法创建角色:{} {} {} {}'.format(account, pid, name, model), 'warning')
        return
    os.mkdir(pid_path)
    # 人物数据
    file = os.path.join(pid_path, 'char.json')
    data = initial_player_data.copy()
    data['名称'] = name
    data['模型'] = model
    data['id'] = pid
    data['性别'] = initial_model_attr[model]['性别']
    data['种族'] = initial_model_attr[model]['种族']
    data['可持有武器'] = initial_model_attr[model]['武器']
    data['可加入门派'] = initial_model_attr[model]['门派']
    data['账号'] = account
    dict2file(data, file)
    redis_set_hash_data(server.redis_conn, str(pid), 'char', data)
    # 物品数据
    file = os.path.join(pid_path, 'item.json')
    data = initial_item_data.copy()
    dict2file(data, file)
    redis_set_hash_data(server.redis_conn, str(pid), 'item', data)
    # 物品仓库数据
    file = os.path.join(pid_path, 'item_warehouse.json')
    data = initial_itemwarehouse_data.copy()
    dict2file(data, file)
    redis_set_hash_data(server.redis_conn, str(pid), 'itemwarehouse', data)
    # 召唤兽数据
    file = os.path.join(pid_path, 'pet.json')
    data = initial_pet_data.copy()
    dict2file(data, file)
    redis_set_hash_data(server.redis_conn, str(pid), 'pet', data)
    # 召唤兽仓库数据
    file = os.path.join(pid_path, 'pet_warehouse.json')
    data = initial_petwarehouse_data.copy()
    dict2file(data, file)
    redis_set_hash_data(server.redis_conn, str(pid), 'petwarehouse', data)

    # account summary添加这个id
    acc_sm[pid] = name
    redis_set_data(server.redis_conn, 'account_summary', acc_sm)
    server.redis_server.save('account_summary')

    sprint('角色已创建:{} {} {} {}'.format(account, pid, name, model))


def player_login(account, passwd, pid):
    print('玩家登陆请求:', account, passwd, pid)
    # 验证密码
    account_path = os.path.join(DATA_PATH, account)
    if not os.path.exists(account_path):
        send(gateway_socket.cur_socket, S_系统提示, dict(内容='账号不存在!'))
        return
    account_config_file = os.path.join(DATA_PATH, account, 'account_config.json')
    account_config_data = file2dict(account_config_file)
    if not str(passwd) == str(account_config_data['password']):
        send(gateway_socket.cur_socket, S_系统提示, dict(内容='账号/密码错误!'))
        return
    else:
        send(gateway_socket.cur_socket, S_系统提示, dict(内容='正在登陆...'))

    pid_path = os.path.join(DATA_PATH, account, str(pid))
    # 角色数据
    file = os.path.join(pid_path, 'char.json')
    data = file2dict(file)
    redis_set_hash_data(server.redis_conn, str(pid), 'char', data)
    send(gateway_socket.cur_socket, S_登陆成功, data)
    # 物品数据
    file = os.path.join(pid_path, 'item.json')
    data = file2dict(file)
    redis_set_hash_data(server.redis_conn, str(pid), 'item', data)
    # 物品仓库数据
    file = os.path.join(pid_path, 'item_warehouse.json')
    data = file2dict(file)
    redis_set_hash_data(server.redis_conn, str(pid), 'item_warehouse', data)
    # 宠物数据
    file = os.path.join(pid_path, 'pet.json')
    data = file2dict(file)
    redis_set_hash_data(server.redis_conn, str(pid), 'pet', data)
    # 宠物仓库数据
    file = os.path.join(pid_path, 'pet_warehouse.json')
    data = file2dict(file)
    redis_set_hash_data(server.redis_conn, str(pid), 'pet_warehouse', data)
