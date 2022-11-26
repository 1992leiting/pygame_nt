import random
from common.socket_id import *
from common.common import *
from common.constants import *
from common.server_process import server


def trigger_npc_dialog(pid, npc_id):
    """
    触发NPC对话
    :param pid:
    :param npc_id:
    :return:
    """
    # TODO: 判断人物和NPC的距离
    if npc_id not in server.npc_objects:
        npc = NPC()
        npc.npc_id = npc_id
        npc.send_msg(pid)
