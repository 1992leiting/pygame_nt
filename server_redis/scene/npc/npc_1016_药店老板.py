
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 101601
        self.name = '药店老板'
        self.title = ''
        self.model = '药店老板'
        self.mx, self.my = 13.5, 18.7
        self.direction = 0
        self.map_id = 1016
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '拉肚子，选好药，选药也要有诀窍','得了病要对症下药，可不能乱吃','是药三分毒，身体有恙，不可不吃药，也不可乱吃','方圆几十里的百姓抓药都要来我这里。'
                ],
            'options':
            [
                '购买','我只是来看看'
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
