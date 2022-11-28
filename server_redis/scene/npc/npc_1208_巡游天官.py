
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 120803
        self.name = '巡游天官'
        self.title = '群雄逐鹿挑战'
        self.model = '巡游天官'
        self.mx, self.my = 166.0, 51.0
        self.direction = 1
        self.map_id = 1208
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你想挑战各个门派的师父吗?来参战群雄逐鹿活动吧'
                ],
            'options':
            [
                '我们要挑战','我来取消任务','算了我还是不去了'
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
