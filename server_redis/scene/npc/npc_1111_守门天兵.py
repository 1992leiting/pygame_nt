
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111103
        self.name = '守门天兵'
        self.title = ''
        self.model = '天兵'
        self.mx, self.my = 238.8, 146.0
        self.direction = 0
        self.map_id = 1111
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '天天在这里守门真是无聊死了，我也渴望冒险刺激的生活','整天有人来打听这打听那的，什么红琉璃白琉璃，当心我火了打你一顿','又要开蟠桃会了，我算算我守了多少年的门，自从我守门开始，已经开了2次蟠桃会了','天宫可是众仙云集之地，不是你想来就来，想走就走的','天宫重地，严禁喧哗！！'
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
