
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 115601
        self.name = '地涌夫人'
        self.title = '门派师傅'
        self.model = '地涌夫人'
        self.mx, self.my = 49.6, 27.6
        self.direction = 1
        self.map_id = 1156
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '不要叫我师父，请叫我女王大人','要想领悟我无底洞技能，可得勤学苦练','我的徒儿们，每一个都那么聪明伶俐','如今，像我这么美貌与智慧并重的好师傅可不多了'
                ],
            'options':
            [
                '交谈','给予','师门任务','学习技能'
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
