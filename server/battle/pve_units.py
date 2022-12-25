"""
PVE战斗的怪物属性
"""
from common.constants import *
from common.common import *

def units_赵捕头战斗测试(*args) -> dict:
    units = {}
    units[0] = dict(
        名称='测试员',
        模型='护卫',
        伤害=150,
        防御=20,
        气血=320,
        灵力=100,
        法防=50,
        躲闪=100,
        魔法=1000,
        速度=20,
        等级=10,
        技能=['高级必杀'],
        主动技能=['水攻']
    )
    units[1] = dict(
        名称='帮手',
        模型='护卫',
        伤害=150,
        防御=20,
        气血=120,
        灵力=100,
        法防=50,
        躲闪=100,
        魔法=1000,
        等级=10,
        速度=18,
        技能=['高级必杀'],
        主动技能=['水攻']
    )
    units[2] = dict(
        名称='帮手',
        模型='护卫',
        伤害=150,
        防御=20,
        气血=120,
        灵力=100,
        法防=50,
        躲闪=100,
        魔法=1000,
        等级=10,
        速度=16,
        技能=['高级必杀'],
        主动技能=['水攻']
    )
    units[3] = dict(
        名称='帮手',
        模型='护卫',
        伤害=150,
        防御=20,
        气血=120,
        灵力=100,
        法防=50,
        躲闪=100,
        魔法=1000,
        等级=10,
        速度=14,
        技能=['高级必杀'],
        主动技能=['水攻']
    )
    units[4] = dict(
        名称='帮手',
        模型='护卫',
        伤害=150,
        防御=20,
        气血=120,
        灵力=100,
        法防=50,
        躲闪=100,
        魔法=1000,
        等级=10,
        速度=12,
        技能=['高级必杀'],
        主动技能=['水攻']
    )
    return units