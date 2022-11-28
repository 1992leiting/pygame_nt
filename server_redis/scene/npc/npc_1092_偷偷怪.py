
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 109211
        self.name = '偷偷怪'
        self.title = ''
        self.model = '兔子怪'
        self.mx, self.my = 135.0, 20.0
        self.direction = 1
        self.map_id = 1092
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '如果你集齐了传送中的五宝（金刚石，定魂珠，龙鳞，夜光珠，避水珠），可以在我这里换特赦令牌哦。集齐笔墨纸砚也可以在我这里兑换炼兽真经'
                ],
            'options':
            [
                '我要换特赦令牌','我要换炼兽真经','熔炼内丹','熔炼高级内丹','我要换点化石','我来看看你'
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
