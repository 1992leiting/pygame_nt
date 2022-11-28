
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111610
        self.name = '蛤蟆勇士'
        self.title = ''
        self.model = '蛤蟆精'
        self.mx, self.my = 195.0, 16.0
        self.direction = 3
        self.map_id = 1116
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '有志青年应该投奔我龙宫，及早谋个好前程啊','我这出去就是海底的迷宫了，里面有不少怪物，最好结伴而行','没事别老找我说话，找那老龟吧，他喜欢侃','嘿哟嘿哟！强身健体，为我龙宫健康工作一万年','真的蛤蟆勇士，敢于直面先天的缺陷。'
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
