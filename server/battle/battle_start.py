from common.common import *
from common.constants import *
from common.socket_id import *
from battle.battle_handler import *


def start_pvp(battle_id, team0: list, team1: list):
    """
    创建PVP转斗, team0/1包含两边的战斗玩家id
    :param team0:
    :param team1:
    :return:
    """
    team0_data = []
    team1_data = []
    for pid in team0:
        pdata = rget(pid, CHAR)
        team0_data.append(pdata)
    for pid in team1:
        pdata = rget(pid, CHAR)
        team1_data.append(pdata)
    battle = Battle(battle_id, team0_data, team1_data)

