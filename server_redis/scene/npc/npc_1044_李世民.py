
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104405
        self.name = '李世民'
        self.title = ''
        self.model = '李世民'
        self.mx, self.my = 48.0, 49.0
        self.direction = 0
        self.map_id = 1044
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '疾风知劲草，板荡识诚臣','凡事要以国家社稷为重','都说为官难，其实要作个好皇帝更难','为君之道，必须先存百姓，若损百姓以奉其身，犹割股以啖腹，腹饱而身毙。若安天下，必须先正其身，未有身正而影曲，上治而下乱者','事不三思，恐怕忙中有错；气能一忍，方知过后无忧。'
                ],
            'options':
            [
                '我要用千亿经验更换兽决','真是个好皇帝'
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
