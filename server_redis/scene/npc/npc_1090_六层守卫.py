
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 109001
        self.name = '六层守卫'
        self.title = ''
        self.model = '周杰伦'
        self.mx, self.my = 70.0, 44.0
        self.direction = 0
        self.map_id = 1090
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我是本层守卫，你每天可以挑战我一次。挑战次数在每日中午12点整刷新。你必须完成前一层的挑战'
                ],
            'options':
            [
                '我要挑战你','我点错了'
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
