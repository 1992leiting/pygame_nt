
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150130
        self.name = '推广使者'
        self.title = '新手推广'
        self.model = '老书生'
        self.mx, self.my = 85.0, 38.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '新玩家可以在我这里填写推广员号后领取新玩家礼包。等级达到60的玩家也可以在我这里生成推广员号，只要填写的推广员号的玩家等级达到50级后即可获得推广奖励。'
                ],
            'options':
            [
                '填写推广员号','生成推广员号','查看推广奖励','我只是路过的'
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
