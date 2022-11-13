
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111602
        self.name = '蟹将军'
        self.title = ''
        self.model = '蟹将'
        self.mx, self.my = 32.0, 100.0
        self.direction = 1
        self.map_id = 1116
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '有志的仙族青年应该投奔我龙宫，及早谋个好前程啊','最近宫里丢了颗定颜珠，千岁正发愁呢','海底地形复杂，当心可别迷了路','一只羊在吃草，一只狼在旁边过，但没吃羊，少侠可知这个谜语说的是谁#40,前几日一只螃蟹爬出蒸锅说“我热”，我愤怒的教导他，想红就给我忍着点#4'
                ],
            'options':
            [
                ''
                ]
        }

    def talk(self, pid, option=None):
        """
        NPC对话
        :param pid: 玩家id
        :param option: 对话选项
        """
        cont = random.sample(self.dialogue['contents'], 1)
        op = self.dialogue['options']

        if option is not None:
            return

        send_data = [S_发送NPC对话, {'模型': self.model, 'id': self.npc_id, '名称': self.name, '对话': cont, '选项': op}]
        GL.DIALOGUE_HISTORY[pid] = send_data
        sk = GL.SOCKETS[pid]
        send(sk, send_data)

npc = NPCX()
