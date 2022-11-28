
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104005
        self.name = '马真人'
        self.title = '召唤兽修炼'
        self.model = '太白金星'
        self.mx, self.my = 127.0, 63.0
        self.direction = 0
        self.map_id = 1040
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '世间万物皆有灵性，平常的召唤兽只要你懂得驾驭的方法，都能让他们发挥出潜在的能力，你想不想提高一下自己控制召唤兽的能力那？'
                ],
            'options':
            [
                '领取任务（100W银币）','跳过本环（消耗银币）','设置修炼类型','管理修炼点数','离开'
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
