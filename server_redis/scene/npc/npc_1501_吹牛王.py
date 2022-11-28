
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150103
        self.name = '吹牛王'
        self.title = ''
        self.model = '装备收购商'
        self.mx, self.my = 91.0, 34.0
        self.direction = 0
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '如果说我现在说的是假话，你相信么？,周猎户最喜欢和我拉家常了，他家就住在药店边上','嘘——千万不要告诉他们我爱吹牛啊，这会影响我的形象的','人生最痛快的事情莫过于和周猎户一起喝点小酒了','天上有只牛在飞，一定是我在地上吹。'
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
