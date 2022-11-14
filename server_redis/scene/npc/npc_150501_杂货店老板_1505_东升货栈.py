
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150501
        self.name = '杂货店老板'
        self.title = ''
        self.model = '超级巫医'
        self.mx, self.my = 35.5, 27.0
        self.direction = 1
        self.map_id = 1505
        self.npc_type = '商店'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '建邺里一年四季温暖如春','客官想买其他杂货可以去城里看看','洞冥草可以解除摄妖香的效果，你记住了吗#1,宠物口粮只能通过怪物获得'
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
