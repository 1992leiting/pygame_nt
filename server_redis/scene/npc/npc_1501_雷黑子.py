
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150127
        self.name = '雷黑子'
        self.title = ''
        self.model = '雷黑子'
        self.mx, self.my = 70.0, 133.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '城里有位好心的郎中陈长寿，给新人看病从不收银子。他一般都在去东海湾的城门口附近摆摊看病','我经常去找宠物仙子姐姐玩，她那里有好多可爱的小动物，上次还送了我一只做宠物呢#43,城里什么都好，就是小伙伴太少。想去江南野外玩，妈妈又不让，说那里的怪物太凶，没一定的修为去了很危险','人之初，性本善，性相近，习相远。教书先生今天教的三字经，我一定得背熟','建邺城里最好吃的就是马氏酸枣了#89'
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
