
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 112301
        self.name = '判官'
        self.title = ''
        self.model = '判官'
        self.mx, self.my = 18.0, 20.0
        self.direction = 0
        self.map_id = 1123
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '生死有命，富贵在天。拜师的请进内室，地藏菩萨正在招收门徒','阎王要你三更死，不敢留你过五更','人生切莫把心欺，神鬼昭彰放过谁？,左执生死簿，右拿勾魂笔，赏善罚恶，管人生死——这说的就是老夫我啦#17'
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
