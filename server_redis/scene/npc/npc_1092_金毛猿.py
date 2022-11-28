
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 109209
        self.name = '金毛猿'
        self.title = ''
        self.model = '老马猴'
        self.mx, self.my = 201.0, 11.0
        self.direction = 0
        self.map_id = 1092
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '幻域迷宫活动已经开放，只要你在迷宫内成功达到20层就可以获得丰厚奖励噢。本活动允许单人或组队参与。'
                ],
            'options':
            [
                '请送我进入迷宫','我是路痴，不适合走迷宫'
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
