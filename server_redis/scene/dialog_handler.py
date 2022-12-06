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
    npc_id = int(npc_id)
    # npc_index = 'npc_{}_{}'.format(NPCS[npc_id]['地图'], NPCS[npc_id]['名称'])
    # if npc_index not in server.npc_objects:
    #     print('npc脚本未找到:', npc_index)
    #     npc = NPC()
    # else:
    #     npc = server.npc_objects[npc_index]
    #
    # npc.npc_id = int(npc_id)

    npc = server.npc_objects[npc_id]
    npc.send(pid)


def trigger_npc_response(pid, npc_id, msg):
    npc_id = str(npc_id)
    npc_index = 'npc_{}_{}'.format(NPCS[npc_id]['地图'], NPCS[npc_id]['名称'])
    if npc_index in server.npc_objects:
        npc = server.npc_objects[npc_index]
        npc.response(pid, msg)
