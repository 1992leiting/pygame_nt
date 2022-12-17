from common.common import *
from common.constants import *
from common.socket_id import *
from threading import Thread
import time
from uuid import uuid4


# 战斗类的状态
ST_等待命令 = 0  # 等待玩家输入命令
ST_战斗计算 = 1  # 进行战斗计算
ST_战斗执行 = 2  # 计算完等玩家返回状态

# 战斗单位的种类
BT_玩家 = 0
BT_召唤兽 = 1
BT_孩子 = 2
BT_怪物 = 3


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
    def __init__(self, id: int, pid0: int, pid1: int, map_id: int=0):
        super().__init__()
        self.is_running = True
        self.battle_id = id
        self.pid0 = pid0
        self.pid1 = pid1
        self.uuid = uuid4()
        self.map_id = map_id
        self.units = empty_indexed_dict(20)  # 所有的战斗单位
        # 如果没有指定地图, 则取发起方所在的地图
        if not self.map_id:
            self.map_id = pget(pid0, CHAR, '地图')
        self.state = ST_等待命令
        self.acting_units = []  # 在执行战斗的单位,按照速度排序之后
        self.battle_process = []  # 战斗流程

    @property
    def num_waiting_for_cmd(self):
        """
        等待下达操作指令的单位数
        :return:
        """
        num = 0  # 没有下达质量的单位数量
        for bu in self.all_valid_units:
            if bu and bu['战斗命令'] == {}:
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
        self.units[pos] = pdata

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

    def set_unit_cmd_by_pos(self, pos, cmd:dict):
        pass

    def start_calculation(self):
        print('执行战斗计算...')
        self.battle_calculation()
        # 计算完更换状态
        self.state = ST_战斗执行
        # 清空所有单位的命令
        for bu in self.all_valid_units:
            if bu:
                bu['战斗命令'] = {}
        # 发送战斗流程给玩家
        for bu in self.all_player_units:
            _pid = bu['id']
            send2pid(_pid, S_战斗流程, dict(流程=self.battle_process))
        # 清空战斗流程
        self.battle_process = []

    def battle_calculation(self):
        # 按照速度排序
        self.acting_units = sorted(self.all_valid_units, key=lambda x: x['速度'], reverse=True)
        for bu in self.acting_units:
            if bu['战斗命令']['类型'] == '攻击':
                self.cal_普通攻击(bu['单位编号'])

    def cal_基础物理伤害(self, attack_id, target_id):
        伤害 = self.units[attack_id]['伤害']
        防御 = self.units[target_id]['防御']
        结果 = 伤害 - 防御
        return 结果

    def cal_最终物理伤害(self, attack_id, target_id, damage):
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
        _process = dict(流程=1, 攻击方=attack_id, 伤害=最终伤害, 目标单位=[dict(编号=target_id, 特效=None)], 返回=True)
        self.battle_process.append(_process)

    def run(self):
        # 战斗开始的数据加载
        self.load_units()  # 加载战斗单位
        # 战斗过程的循环
        while self.is_running:
            # 等待战斗单位下达指令
            if self.state == ST_等待命令:
                if self.num_waiting_for_cmd <= 0:  # 所有单位指令下达则进入执行计算
                    self.state = ST_战斗计算
            # 计算完成后进入执行计算
            elif self.state == ST_战斗计算:
                self.start_calculation()
            time.sleep(0.01)
