
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150110
        self.name = '陈长寿'
        self.title = ''
        self.model = '药店老板'
        self.mx, self.my = 220.0, 21.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这建邺小城真是风景如画','十级以下的新人我可以为你免费治疗伤势','我是行走江湖的郎中，治病救人是我份内之事','我是建邺城最精通医药之术的人','少肉多菜，少烦多眠，少欲多施，方能长寿。'
                ],
            'options':
            [
                '快些治疗我吧','我点错了'
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
