
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 153202
        self.name = '含冤小白龙'
        self.title = ''
        self.model = '小白龙'
        self.mx, self.my = 35.0, 9.0
        self.direction = 0
        self.map_id = 1532
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '在海里呆得久了，想到陆地上走走','龙王正在广招门徒，这几天来拜师的人越来越多了','龙宫里有数不尽的宝贝，有机缘之人才能得到。听巡逻虾兵说附近来了条小龙，不过好象鬼鬼祟祟的，莫非有什么企图不成？,咱龙王老爷就在我身后的大殿里，不过可不是什么人都能进去的！'
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
