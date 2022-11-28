
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104003
        self.name = '仓库管理员'
        self.title = '管理仓库'
        self.model = '商会总管'
        self.mx, self.my = 114.0, 87.0
        self.direction = 0
        self.map_id = 1040
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这人在江湖久了就难免多了些物品，我这里的仓库那可是数一数二的，绝对让您放心。'
                ],
            'options':
            [
                '打开仓库','购买仓库(消耗50万银子)','取消'
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
