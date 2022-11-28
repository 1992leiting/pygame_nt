
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 97
        self.name = '回收商人'
        self.title = ''
        self.model = '钱庄老板'
        self.mx, self.my = 247.0, 110.0
        self.direction = 1
        self.map_id = 1001
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '如果你想回收（魔兽要诀，高级魔兽要诀，特殊魔兽要诀），可以在我这里换积分哦。'
                ],
            'options':
            [
                '回收魔兽要诀','回收高级魔兽要诀','回收特殊魔兽要诀','我来看看你'
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
