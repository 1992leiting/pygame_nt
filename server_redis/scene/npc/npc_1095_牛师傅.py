
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 109501
        self.name = '牛师傅'
        self.title = ''
        self.model = '服装店老板'
        self.mx, self.my = 16.0, 19.0
        self.direction = 0
        self.map_id = 1095
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '听说世间最美的服饰出自月宫嫦娥之手','客官想要什么样的衣服？,长木匠，短铁匠，不长不短是裁缝。'
                ],
            'options':
            [
                '购买','我什么都不想做'
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
