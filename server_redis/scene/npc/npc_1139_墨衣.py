
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 113902
        self.name = '墨衣'
        self.title = ''
        self.model = '修罗傀儡妖'
        self.mx, self.my = 4.0, 54.0
        self.direction = 0
        self.map_id = 1139
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我们似乎已经在此处待了很久很久了','红莲那丫头的性子，还是那么莽撞冲动，真是伤脑筋啊#83,能来到这里，真是一段难得的缘分呢……'
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
