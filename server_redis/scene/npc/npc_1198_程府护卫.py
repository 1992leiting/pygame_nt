
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 119803
        self.name = '程府护卫'
        self.title = ''
        self.model = '护卫'
        self.mx, self.my = 89.0, 95.0
        self.direction = 0
        self.map_id = 1198
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '程老爷三板斧，你学到第几斧啦？,能拜我们程老爷为师可是一种荣幸呢','府衙禁地，闲杂人等不得入内','这里是天子脚下，太平得很,大唐首席弟子之争日趋白热。'
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
