from common.common import *
from common.constants import *
from common.socket_id import *
from battle.battle_handler import *


def start_pvp(battle_id, pid0, pid1, *args):
    """
    创建PVP转斗, team0/1包含两边的战斗玩家id
    :param battle_id:
    :param pid1: 发起方pid
    :param pid1: 被发起方pid
    :return:
    """
    battle = Battle(battle_id, pid0, pid1)  # battle线程
    server.battles.append(battle)
    battle.start()

