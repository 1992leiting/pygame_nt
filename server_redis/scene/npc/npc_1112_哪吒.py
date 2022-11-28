
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111205
        self.name = '哪吒'
        self.title = ''
        self.model = '哪吒'
        self.mx, self.my = 65.7, 46.8
        self.direction = 0
        self.map_id = 1112
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '居然把火尖枪输给那个看门小神，那是师傅送我的枪啊#52我有何颜面去见师傅和父亲,作为三坛海会大神，率领天兵去收降那猴子，却屡战屡败，真是惭愧','下界有妖魔作乱，要多加防范才是','天上一日，人间一年。下界许久没什么大动静，我待在这都快生锈了','莲藕为骨，荷叶为衣，我乃刀枪不入之躯。'
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
