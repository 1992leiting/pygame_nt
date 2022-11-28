
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 101901
        self.name = '颜如玉'
        self.title = ''
        self.model = '老书生'
        self.mx, self.my = 18.0, 20.0
        self.direction = 0
        self.map_id = 1019
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '从小我就一直在努力学习，现在还是在学习，多学多问#101，要不要过来帮帮忙呢?我可以付工钱!'
                ],
            'options':
            [
                '是的我要打工','我来制作灵饰图鉴','我还是在考虑考虑'
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
