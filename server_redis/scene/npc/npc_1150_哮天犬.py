
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 115002
        self.name = '哮天犬'
        self.title = ''
        self.model = '哮天犬'
        self.mx, self.my = 77.0, 36.0
        self.direction = 1
        self.map_id = 1150
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '啊呜啊呜……汪汪汪','天庭里那个二郎神长得好像和主人不是很像……,跟随主人出生入死这么多年，我们一起经历了许多事情，不知道你想听我从那一件讲起呢？'
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
