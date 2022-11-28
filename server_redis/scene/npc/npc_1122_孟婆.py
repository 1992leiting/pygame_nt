
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 112205
        self.name = '孟婆'
        self.title = ''
        self.model = '老太婆'
        self.mx, self.my = 99.5, 94.5
        self.direction = 0
        self.map_id = 1122
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '相见不如怀念，怀念不如忘记','喝下孟婆汤，过了奈何桥，前生的事就再与你无缘','孟婆汤有甘、苦、辛、酸、咸五种口味，少侠想要哪一种？,听说地藏菩萨在广招门徒，年轻人想不想去学些本领？'
                ],
            'options':
            [
                ''
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
