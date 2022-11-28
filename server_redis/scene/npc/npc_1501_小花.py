
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150117
        self.name = '小花'
        self.title = ''
        self.model = '小花'
        self.mx, self.my = 207.0, 108.0
        self.direction = 0
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '面对世俗偏见，有情人终成眷属真的不容易#52,货栈边上那个王大嫂做的烤鸭真是好吃,又过冬了，得为咱家孩子添置几件棉袄了,听说最近长安城集市热闹的很，过几天可要去看看,听说东海里有数不尽的宝贝……'
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
