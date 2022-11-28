
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 99
        self.name = '后羿英魂'
        self.title = '角色化圣'
        self.model = '进阶狂豹人形'
        self.mx, self.my = 446.0, 47.0
        self.direction = 1
        self.map_id = 1001
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '只有正在的英雄才能获得三足金乌的力量，所有，少侠，你就是我选中的人！'
                ],
            'options':
            [
                '我要领取化圣任务','我要提升化圣境界（修炼提升）','我要沐浴金乌光芒','我要恢复任务','我来看看大英雄'
                ]
        }

    def talk(self, pid, content=None, option=None):
        """
        NPC对话
        """
        cont = random.sample(self.dialogue['contents'], 1)
        op = self.dialogue['options']

        if content is not None:
            cont = content
        if option is not None:
            op = option

        send_data = {'模型': self.model, 'npc_id': self.npc_id, '名称': self.name, '对话': cont, '选项': op, '类型': 'npc'}
        send2pid(pid, S_发送NPC对话, send_data)
    
    def response(self, pid, msg):
        pass

npc = NPCX()
