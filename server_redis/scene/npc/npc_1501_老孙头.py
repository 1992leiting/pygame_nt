
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150109
        self.name = '老孙头'
        self.title = ''
        self.model = '马货商'
        self.mx, self.my = 223.0, 12.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '几年前一次台风，这里沉了不少船，东海湾那里常年有个旋涡，沉掉的船都在下面。要下沉船，从海边的旋涡那潜下去即可','要下沉船，从海边的旋涡那潜下去即可','这几年风调雨顺，老百姓的日子过得都很富足，只是城外野兽横行，常有外出的百姓受到骚扰。'
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
