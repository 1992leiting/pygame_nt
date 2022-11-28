
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114101
        self.name = '观音姐姐'
        self.title = '门派师傅'
        self.model = '观音姐姐'
        self.mx, self.my = 12.0, 11.0
        self.direction = 0
        self.map_id = 1141
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '观世间疾苦繁华，身身入耳，一一在心','我南海普陀山有救世正心之法，只传授给有缘之人','心欲若除，则万事可成，心无杂念，非外事可扰','佛祖有真经三藏，乃是修真之经，正善之门，可劝人为善','修行贵在持之以恒，切忌浮躁自满。'
                ],
            'options':
            [
                '交谈','给予','师门任务','学习技能'
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
