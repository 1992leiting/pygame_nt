
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150115
        self.name = '超级巫医'
        self.title = '召唤兽治疗师'
        self.model = '超级巫医'
        self.mx, self.my = 211.0, 46.0
        self.direction = 0
        self.map_id = 1501
        self.npc_type = '超级巫医'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我是专门治疗和调训召唤兽的医生，10级以下免费治疗驯养，选择驯养或治疗之前请注意：我每次都是把你身上携带的所有召唤兽进行统一治疗和驯养'
                ],
            'options':
            [
                '我的召唤兽受伤了请帮我救治一下吧','我的召唤兽忠诚度降低了请帮我驯养一下吧','我要同时补满召唤兽的气血、魔法和忠诚值','重置召唤兽属性点(消耗300万银子)','我只是看看'
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
