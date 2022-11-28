
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 115401
        self.name = '巫奎虎'
        self.title = '门派师傅'
        self.model = '巫奎虎'
        self.mx, self.my = 33.5, 32.0
        self.direction = 0
        self.map_id = 1154
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '大家往来神木之上，切记这里的一草一木，均有神灵在，不可以随便踩到花花草草哦','我神木林一派擅长操控自然之灵，天地万物均可化为己用，但谨记必须对神灵心存敬畏，方能运用自如','神木林千百年幽闭在武神坛之上，现在打开门户广纳门派，来来往往热闹了许多，突然有点不习惯#17,我违背先祖遗训，打开了神木林的大门，让我族法传承出去，这究竟是对是错，全看徒儿你们是否真能为三界安危尽一份力了……'
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
