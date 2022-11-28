
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 110101
        self.name = '杜天'
        self.title = ''
        self.model = '兰虎'
        self.mx, self.my = 21.0, 18.0
        self.direction = 0
        self.map_id = 1101
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '少侠是来选购兵器的吧？请慢慢挑选，务必看清楚名称哦','这里的风景还不错吧','客官想要什么兵器？,行走江湖不能两手空空，来挑一件趁手的兵器吧。'
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
