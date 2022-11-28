
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 115001
        self.name = '二郎神'
        self.title = '门派师傅'
        self.model = '二郎神'
        self.mx, self.my = 68.0, 32.0
        self.direction = 1
        self.map_id = 1150
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '能给我杨戬当徒儿的，都是人中龙凤','想听故事找你们那六个师叔去，为师忙得很','好久没和孙悟空那小子比试比试了，真是寂寞如雪啊','为师教给你的东西可都学会了？'
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
