import random
from common.socket_id import *
from common.common import *
from common.constants import *
from common.server_process import server


class NPC:
    def __init__(self) -> None:
        self.npc_id = 0
        self.name = 'NPC'
        self.title = None
        self.model = '男人_苦力'
        self.mx, self.my = 0, 0
        self.direction = 0  # 方向, 0 ↘, 1 ↓, 2 ↙, 3 →, 4 ←, 5 ↗, 6 ↑, 7 ↖
        self.map_id = 1001
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {'contents': ['你找我有事吗?'], 'options': []}

    def talk(self, pid, option=None):
        cont = random.sample(self.dialogue['contents'], 1)
        op = self.dialogue['options']

        send_data = {'模型': self.model, 'npc_id': self.npc_id, '名称': self.name, '对话': cont, '选项': op}
        send2pid(pid, S_发送NPC对话, send_data)


def player_enter_scene(pid, map_id):
    # 发送所有npc
    # for npc in NPCS:
    #     if npc.map_id == map_id:
    #         npc_data = {
    #             'npc_id': npc.npc_id,
    #             '名称': npc.name,
    #             '称谓': npc.title,
    #             '模型': npc.model,
    #             'mx': npc.mx,
    #             'my': npc.my,
    #             '方向': npc.direction,
    #             '地图': npc.map_id,
    #             'NPC类型': npc.npc_id
    #         }
    i = 0
    for npc in NPCS.values():
        if int(npc['地图']) == map_id:
            i += 1
            npc_data = {
                'id': i,
                '名称': npc['名称'],
                '称谓': npc['称谓'],
                '模型': npc['模型'],
                'mx': npc['x'],
                'my': npc['y'],
                '方向': npc['方向'],
                '地图': npc['地图'],
                'NPC类型': npc['类型']
            }
            send2pid(pid, S_NPC数据, npc_data)


def scene_transfer():
    pass
