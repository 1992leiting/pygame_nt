
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 52
        self.name = '梦倾笙'
        self.title = '无限轮回挑战'
        self.model = '渡劫神天兵'
        self.mx, self.my = 237.0, 105.0
        self.direction = 1
        self.map_id = 7052
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '如果你的等级达到了69级且对自己的属性很有自信就可以在我这里进行连续20关的无限轮回挑战。只要成功通过第一关就能获得奖励。'
                ],
            'options':
            [
                '我要挑战(切入战斗)','难度太高了','我放弃'
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
