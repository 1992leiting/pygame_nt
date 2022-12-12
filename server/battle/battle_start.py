from common.common import *
from common.constants import *
from common.socket_id import *
from battle.battle_handler import *


def start_pvp(battle_id, team0: list, team1: list):
    """
    创建PVP转斗, team0/1包含两边的战斗玩家id
    :param team0: 发起方pid列表
    :param team1: 被发起方pid列表
    :return:
    """
    team0_data = []
    team1_data = []
    for pid in team0:
        pdata = server.players[pid][CHAR]
        team0_data.append(pdata)
    for pid in team1:
        pdata = server.players[pid][CHAR]
        team1_data.append(pdata)
    battle = Battle(battle_id, team0_data, team1_data)
    # 发送战斗信息
    for p in team0:
        send2pid(p, S_开始战斗, dict(我方=team0_data, 敌方=team1_data))
    for p in team1:
        send2pid(p, S_开始战斗, dict(我方=team1_data, 敌方=team0_data))

