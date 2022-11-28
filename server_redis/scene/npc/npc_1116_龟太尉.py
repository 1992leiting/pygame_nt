
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111607
        self.name = '龟太尉'
        self.title = ''
        self.model = '龟丞相'
        self.mx, self.my = 53.0, 16.0
        self.direction = 2
        self.map_id = 1116
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '有志青年应该投奔我龙宫，及早谋个好前程啊','整天就是在这里看门，真是没什么意思，不过真让我休息的话我也还是找个地方待着睡觉','千年王八万年龟，我今年已经一万零八岁了','学游泳，找我就对了，价格实惠，包学包会#39,这太尉不过是个有名无实的闲职罢了！'
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
