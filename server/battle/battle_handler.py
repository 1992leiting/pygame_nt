from common.common import *
from common.constants import *
from common.socket_id import *
from common.battle_id import *
from threading import Thread
import time
from uuid import uuid4


# 战斗类的状态
ST_等待命令 = 0  # 等待玩家输入命令
ST_战斗计算 = 1  # 进行战斗计算
ST_战斗执行 = 2  # 计算完等玩家返回状态


class Unit:
    def __init__(self):
        self.type = BT_怪物
        self.team_id = 0  # 0/1, teams0/teams1
        self.data = {}  # 单位的常规属性,非战斗属性
        self.cmd = {}  # 操作指令

    def load_from_bu_data(self, data: dict):
        self.data = data
        return self


class Battle(Thread):
    def __init__(self, id: int, pid0: int, pid1: int, map_id: int=0, pve_units=None):
        super().__init__()
        self.is_running = True
        self.battle_id = id
        self.pid0 = pid0
        self.pid1 = pid1
        self.uuid = uuid4()
        self.map_id = map_id
        self.pve_units = pve_units
        self.units = empty_indexed_dict(20)  # 所有的战斗单位
        # 如果没有指定地图, 则取发起方所在的地图
        if not self.map_id:
            self.map_id = pget(pid0, CHAR, '地图')
        self.acting_units = []  # 在执行战斗的单位,按照速度排序之后
        self.battle_process = []  # 战斗流程
        self.winning_camp = None  # 胜利方
        self.battle_end = False  # 战斗结束标志位

        self.state = ST_等待命令

    @property
    def num_waiting_for_cmd(self):
        """
        等待下达操作指令的单位数
        :return:
        """
        num = 0  # 没有下达质量的单位数量
        for bu in self.all_valid_units:
            if bu['战斗命令'] == {}:
                num += 1
        return num

    @property
    def num_waiting_for_battle_process_end(self):
        num = 0
        for bu in self.all_player_units:
            if bu and not bu['战斗执行完成']:
                num += 1
        return num

    @property
    def all_player_units(self) -> list:
        """
        所有的玩家单位
        :return:
        """
        pu = []
        for bu in self.all_valid_units:
            if bu and bu['单位类型'] == BT_玩家:
                pu.append(bu)
        return pu

    @property
    def all_valid_units(self) -> list:
        """
        所有有效的战斗单位(非None)
        :return:
        """
        vu = []
        for bu in self.units.values():
            if bu:
                vu.append(bu)
        return vu

    @property
    def team0_valid_units(self):
        vu = []
        for bu in self.units.values():
            if bu and bu['阵营'] == 0:
                vu.append(bu)
        return vu

    @property
    def team1_valid_units(self):
        vu = []
        for bu in self.units.values():
            if bu and bu['阵营'] == 1:
                vu.append(bu)
        return vu

    def load_units(self):
        """
        战斗开始时加载所有战斗单位
        :return:
        """
        # ----------team0----------
        # TODO:判断是否有队伍
        pos = 0
        # if pget(self.pid0, CHAR, '队伍id'):
        #     pass
        # else:
        self.load_player_unit(self.pid0, pos)

        # ----------team1----------
        # TODO:判断是否有队伍
        pos = 10
        if self.pid1:
            # if pget(self.pid1, CHAR, '队伍id'):
            #     pass
            # else:
            self.load_player_unit(self.pid1, pos)
        elif self.pve_units:
            for i, unit in self.pve_units.items():
                self.load_pve_unit(unit, pos + i)
            self.set_pve_unit_cmd()  # 回合开始设置PVE单位战斗命令

        print('加载战斗单位完成:', self.units)

        # ----------发送战斗数据----------
        # 阵营为0则0-9在观战方/10-19在对战方, 阵营为1则相反
        for pu in self.all_player_units:
            _pid = pu['id']
            send2pid(_pid, S_开始战斗, dict(单位信息=self.units, 阵营=pu['阵营']))

    def load_player_unit(self, pid, pos):
        """
        加载玩家单位
        :param pid: 玩家pid
        :param pos: 队伍站位
        :return:
        """
        team_id = 0
        if pos >= 10:
            team_id = 1
        pdata = pget(pid, CHAR, '').copy()
        pdata['单位类型'] = BT_玩家
        pdata['阵营'] = team_id
        pdata['单位编号'] = pos
        pdata['战斗命令'] = {}
        pdata['战斗执行完成'] = False
        pdata['死亡'] = False
        pdata['技能'] = []
        pdata['主动技能'] = ['牛刀小试', '鹰击']
        self.units[pos] = pdata
        send2pid(pid, S_战斗主动技能, dict(主动技能=pdata['主动技能']))

    def load_pve_unit(self, unit_data, pos):
        """
        加载PVE单位
        :param unit_data:
        :param pos:
        :return:
        """
        if '单位类型' not in unit_data:
            unit_data['单位类型'] = BT_怪物
        if '最大气血' not in unit_data:
            unit_data['最大气血'] = unit_data['气血']
        if '最大魔法' not in unit_data:
            unit_data['最大魔法'] = unit_data['魔法']
        if '愤怒' not in unit_data:
            unit_data['愤怒'] = 0
        unit_data['阵营'] = 1
        unit_data['单位编号'] = pos
        unit_data['战斗命令'] = {}
        unit_data['战斗执行完成'] = False
        unit_data['死亡'] = False
        self.units[pos] = unit_data

    def get_unit_id_by_pid(self, pid):
        for bu in self.all_player_units:
            if bu['id'] == pid:
                return bu['单位编号']
        return None

    def set_unit_cmd_by_pid(self, pid, cmd:dict):
        """
        根据pid设置玩家命令, 包含人物命令和召唤兽命令
        :param pid:
        :param cmd:
        :return:
        """
        char_cmd = cmd['0']
        pet_cmd = cmd['1']
        # 人物命令
        unit_id = self.get_unit_id_by_pid(pid)
        self.units[unit_id]['战斗命令'] = char_cmd
        # TODO:召唤兽命令
        pass

    def set_pve_unit_cmd(self):
        """
        设置所有PVE单位的命令
        :return:
        """
        if self.battle_id == B_赵捕头战斗测试:
            for bu in self.team1_valid_units:
                bu['战斗命令'] = dict(类型='攻击', 目标=0, 阵营=0, 参数=None, 附加=None)
                print('PVE单位命令', bu['名称'], bu['战斗命令'])

    def set_unit_param_by_pid(self, pid, param, value):
        unit_id = self.get_unit_id_by_pid(pid)
        self.units[unit_id][param] = value

    def can_unit_act(self, unit_id):
        unit = self.units[unit_id]
        if unit['死亡']:
            return False
        return True

    def start_calculation(self):
        print('执行战斗计算...')
        self.cal_准备计算()
        # 计算完更换状态
        self.state = ST_战斗执行
        # 清空一些参数
        for bu in self.all_valid_units:
            if bu:
                bu['战斗命令'] = {}
                bu['战斗执行完成'] = False
        # 发送战斗流程给玩家
        for bu in self.all_player_units:
            _pid = bu['id']
            send2pid(_pid, S_战斗流程, dict(流程=self.battle_process))
        # 清空战斗流程
        self.battle_process = []

    def pick_enemy_units(self, battle_id, target0, num):
        target_list = [target0]
        if self.units[battle_id]['阵营'] == 1:
            pick_list = self.team0_valid_units.copy()
        else:
            pick_list = self.team1_valid_units.copy()
        for unit in pick_list:
            if unit['单位编号'] == target0:
                pick_list.remove(unit)
        sorted(pick_list, key=lambda x: x['速度'], reverse=True)
        num = min(num, len(target_list))
        return target_list[:num]

    def pick_my_units(self, battle_id, target0, num):
        target_list = [target0]
        return target_list

    def cal_战斗结算(self) -> bool:
        """
        判断战斗是否结束
        :return:
        """
        # ----------一方战斗单位全部死亡----------
        num_alive = len(self.team0_valid_units)
        for bu in self.team0_valid_units:
            if bu['死亡']:
                num_alive -= 1
        if num_alive <= 0:
            self.winning_camp = 1
            print('team0全部死亡')
            return True
        num_alive = len(self.team1_valid_units)
        for bu in self.team1_valid_units:
            if bu['死亡']:
                self.winning_camp = 0
                num_alive -= 1
        if num_alive <= 0:
            print('team1全部死亡')
            return True
        # 默认返回False
        return False

    def cal_准备计算(self):
        # 按照速度排序
        self.acting_units = sorted(self.all_valid_units, key=lambda x: x['速度'], reverse=True)
        for bu in self.acting_units:
            if self.can_unit_act(bu['单位编号']):
                if bu['战斗命令']['类型'] == '攻击':
                    self.cal_普通攻击(bu['单位编号'])
                # 每个单位执行动作之后都判断战斗是否结束
                self.battle_end = self.cal_战斗结算()
                if self.battle_end:
                    break

    def cal_基础物理伤害(self, attack_id, target_id):
        """
        基础属性/修炼, 和非物理伤害结果相关的计算
        :param attack_id:
        :param target_id:
        :return:
        """
        伤害 = self.units[attack_id]['伤害']
        防御 = self.units[target_id]['防御']
        结果 = 伤害 - 防御
        结果 = int(结果 * random.randint(90, 110)/100)  # 10%的波动
        return 结果

    def cal_最终物理伤害(self, attack_id, target_id, damage):
        """
        对最终物理伤害结果生效的计算放在这里
        :param attack_id:
        :param target_id:
        :param damage:
        :return:
        """
        return damage

    def cal_普通攻击(self, attack_id):
        target_id = self.units[attack_id]['战斗命令']['目标']
        必杀 = False  # 必杀
        躲避 = False  # 躲避
        防御 = False  # 挨打方主动防御
        反震 = 0  # 反震伤害
        反击 = False  # 反击
        保护 = False  # 保护

        伤害 = self.cal_基础物理伤害(attack_id, target_id)
        最终伤害 = self.cal_最终物理伤害(attack_id, target_id, 伤害)
        if 最终伤害 <= 0:
            最终伤害 = 1
        death = self.unit_hp_drop(target_id, 最终伤害, attack_id)  # 挨打方是否死亡
        _process = dict(流程=1, 攻击方=attack_id, 伤害=dict(数值=最终伤害, 类型=DAMAGE), 目标单位=[dict(编号=target_id, 特效=None, 死亡=death)], 返回=True)
        self.battle_process.append(_process)

    def cal_法术计算(self, attack_id):
        法术名称 = self.units[attack_id]['战斗命令']['参数']
        目标 = self.units[attack_id]['战斗命令']['目标']
        法术等级 = 1  # TODO:法术等级判断

        if 法术名称 in SK_物攻技能:
            self.cal_物攻技能(attack_id, 目标, 法术名称, 法术等级)

    def cal_物攻技能(self, attack_id, target_id, name, lv):
        点选目标 = target_id
        目标数 = 3  # TODO:取技能目标数
        目标 = self.pick_enemy_units(attack_id, 点选目标, 目标数)

    def unit_hp_drop(self, target_id, value, attack_id=None, magic_name=None) -> bool:
        """
        单位掉血
        :param target_id: 掉血对象
        :param value: 掉血数值
        :param attack_id: 攻击方id
        :param magic_name: 法术名称
        :return:
        """
        # 减少气血: 气血/气血上限/最大气血, TODO: 处理伤势
        self.units[target_id]['气血'] -= value
        if self.units[target_id]['气血'] < 0:
            self.units[target_id]['气血'] = 0
            self.units[target_id]['死亡'] = True
        return self.units[target_id]['死亡']

    def send_player_hp_data(self):
        """
        给所有玩家发送血量/魔法/愤怒信息
        :return:
        """
        hp_data = [{}, {}]  #  人物/召唤兽
        for bu in self.all_valid_units:
            hp_data[0] = dict(
                气血=bu['气血'],
                最大气血=bu['最大气血'],
                魔法=bu['魔法'],
                最大魔法=bu['最大魔法'],
                愤怒=bu['愤怒'],
            )
            # TODO:召唤兽

            for u in self.all_player_units:
                if u['阵营'] == bu['阵营']:
                    send2pid(bu['id'], S_战斗血量数据, dict(单位编号=u['单位编号'], 数据=hp_data))

    def exit_battle(self):
        """
        退出战斗
        :return:
        """
        if self.battle_id == B_玩家切磋:
            for bu in self.all_player_units:
                if bu['死亡']:
                    send2pid(bu['id'], S_系统提示, dict(内容='#R你在PK战斗中死亡了#14'))
        for bu in self.all_player_units:
            send2pid(bu['id'], S_退出战斗, {})
        self.is_running = False
        server.battles.remove(self)


    def run(self):
        # 战斗开始的数据加载
        self.load_units()  # 加载战斗单位
        self.send_player_hp_data()  # 发送血量数据
        # 战斗过程的循环
        while self.is_running:
            # 等待战斗单位下达指令
            if self.state == ST_等待命令:
                if self.num_waiting_for_cmd <= 0:  # 所有单位指令下达则进入执行计算
                    self.state = ST_战斗计算
            # 计算完成后进入战斗计算
            elif self.state == ST_战斗计算:
                self.start_calculation()
            # 战斗执行阶段,等待所有单位客户端动画执行完成
            elif self.state == ST_战斗执行:
                if self.num_waiting_for_battle_process_end <= 0:  # 所有单位执行完成
                    if self.battle_end:  # 战斗结束
                        self.exit_battle()
                    # 战斗未结束, 进入命令状态
                    self.send_player_hp_data()  # 刷新血量数据
                    for bu in self.all_player_units:
                        _pid = bu['id']
                        send2pid(_pid, S_战斗命令状态, {})
                    self.state = ST_等待命令
                    # 如果是PVE战斗, 自动设置PVE单位命令
                    if self.pve_units:
                        self.set_pve_unit_cmd()
            time.sleep(0.01)
