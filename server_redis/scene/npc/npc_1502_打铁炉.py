
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150203
        self.name = '打铁炉'
        self.title = ''
        self.model = '打铁炉'
        self.mx, self.my = 28.0, 17.0
        self.direction = 0
        self.map_id = 1502
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '（这是一个燃着暗红色火光的打铁炉，使用的时候请小心，烫到手就不好了。）'
                ],
            'options':
            [
                '查看熟练度','打造','合成','修理','分解','熔炼'
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
