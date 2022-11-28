
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 113701
        self.name = '菩提祖师'
        self.title = '门派师傅'
        self.model = '菩提祖师'
        self.mx, self.my = 45.0, 30.0
        self.direction = 1
        self.map_id = 1137
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '难！难！难！道最玄，莫把金丹做等闲。不遇至人传妙诀，空言口困舌头干','天地玄黄修道德，宇宙洪荒炼元神；虎龙啸聚风云鼎，乌兔周旋卯酉晨','我方寸山的技艺只传授有缘之人,修行贵在用心领悟，切忌轻浮自满','方寸何意，三星又何意，徒儿你可明白？,修习之路没有捷径，踏平坎坷方能成大道。'
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
