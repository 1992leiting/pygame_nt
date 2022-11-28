
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 186502
        self.name = '红色机关人'
        self.title = ''
        self.model = '帮派机关人'
        self.mx, self.my = 25.0, 14.0
        self.direction = 1
        self.map_id = 1835
        self.npc_type = '传送'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我是本帮的机关人，请问你需要进行什么操作？'
                ],
            'options':
            [
                '送我去聚义厅','送我去书院','送我去金库','送我去厢房','送我去兽室','送我去仓库','送我去长安城','我是来破坏你的','取消'
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
