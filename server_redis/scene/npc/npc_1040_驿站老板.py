
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104002
        self.name = '驿站老板'
        self.title = '传送丝绸之路'
        self.model = '驿站老板'
        self.mx, self.my = 15.0, 114.0
        self.direction = 0
        self.map_id = 1040
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '少侠欲前往丝绸之路吗？'
                ],
            'options':
            [
                '我去！我去！','我路过瞧瞧而已'
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
