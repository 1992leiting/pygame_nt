
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 100702
        self.name = '奔波儿'
        self.title = ''
        self.model = '蛤蟆精'
        self.mx, self.my = 115.0, 31.0
        self.direction = 0
        self.map_id = 1007
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我叫做弃波儿法。是乱石山碧波潭万圣龙王手下的蛤蟆精。我家万圣公主招得一个驸马唤做九头精怪，神通广天。日前显法力下了一阵血雨，借机偷了镇塔之宝。驸马偷宝之后怕人发觉，故差我在此看守，这是公主赐给我的白剑。'
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
