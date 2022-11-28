
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 113503
        self.name = '觉案'
        self.title = ''
        self.model = '道士'
        self.mx, self.my = 108.0, 43.0
        self.direction = 1
        self.map_id = 1135
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '方寸山远离红尘，清净雅致，正适合修道炼丹','方寸山以用符出名，方寸山的弟子人人都会画两手符','修道贵在专心，一心向道才能学有所成','由迷茫到觉悟的境界即是觉岸。可是苦海无边，哪里才是岸啊？,是谁在此喧哗？打扰了我的清修#4'
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
