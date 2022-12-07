from common.common import *
from common.constants import *
from common.socket_id import *


# 战斗类的状态
ST_等待玩家指令 = 0
ST_执行计算 = 1

# 战斗单位的种类
BT_玩家 = 0
BT_召唤兽 = 1
BT_孩子 = 2
BT_怪物 = 3


class Unit:
    def __init__(self):
        self.type = BT_怪物
        self.team = 0  # 0/1, teams0/teams1
        self.data = {}  # 单位的常规属性,非战斗属性
        self.cmd = {}  # 操作指令

    def load_from_bu_data(self, data: dict):
        self.data = data
        if '类型' in data:
            self.type = data['类型']
        if 'type' in data:
            self.type = data['type']
        return self


class Battle:
    def __init__(self, id: int, team0: list, team1: list):
        self.battle_id = id
        self.uuid = ''
        self.state = ST_等待玩家指令
        self.team0 = empty_indexed_dict(10)
        self.team1 = empty_indexed_dict(10)
        for i, bu in enumerate(team0):
            unit = Unit().load_from_bu_data(data)
            unit.team = 0

    def update(self):
        if self.state == ST_等待玩家指令:
            pass
        elif self.state == ST_执行计算:
            pass
