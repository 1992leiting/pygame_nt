
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 95
        self.name = '剧情使者'
        self.title = '剧情领取'
        self.model = '雪眸影_七彩神驴_剑侠客'
        self.mx, self.my = 439.0, 55.0
        self.direction = 1
        self.map_id = 1001
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '针对剧情不会触发的玩家补领一次。'
                ],
            'options':
            [
                '领取玄奘的身世','领取含冤小白龙','领取三打白骨精','领取商人的鬼魂'
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
