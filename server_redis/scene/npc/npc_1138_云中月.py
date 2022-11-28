
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 113802
        self.name = '云中月'
        self.title = ''
        self.model = '巫师'
        self.mx, self.my = 22.0, 68.0
        self.direction = 0
        self.map_id = 1138
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '远古的祖先留下训言，神木族将有三次灾祸，现如今巫神女之乱和虎魄之乱均已灵验，还有一次……,咳咳，俺们神木林千百年来遵守于黄帝大人的约定，如今灾乱四起，不得不踏进江湖，这究竟是福还是祸……'
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
