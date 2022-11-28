
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 102801
        self.name = '店小二'
        self.title = '挖宝图任务'
        self.model = '小二'
        self.mx, self.my = 11.0, 30.0
        self.direction = 0
        self.map_id = 1028
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '别看我只是一个小二，长安消息可就数我最灵通了，最近在这里住店过往商人经常提起有强盗的事情，想不想听听？'
                ],
            'options':
            [
                '听听无妨。。。(消耗2000两银子)','还是别多管闲事了。。。'
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
