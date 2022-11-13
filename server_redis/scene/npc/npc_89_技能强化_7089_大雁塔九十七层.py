
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 89
        self.name = '技能强化'
        self.title = '强化技能学习'
        self.model = '书生'
        self.mx, self.my = 30.0, 17.0
        self.direction = 1
        self.map_id = 7089
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我是城里的教书先生，如果你不清楚接下来做些什么，我可以给你一些建议','黑发不知勤学早，白首方悔读书迟。少侠可不要荒废了学业','在我教过的学生里，雷黑子是最刻苦上进的一个。'
                ],
            'options':
            [
                '强化技能','我随便逛逛不好意思'
                ]
        }

    def talk(self, pid, option=None):
        """
        NPC对话
        :param pid: 玩家id
        :param option: 对话选项
        """
        cont = random.sample(self.dialogue['contents'], 1)
        op = self.dialogue['options']

        if option is not None:
            return

        send_data = [S_发送NPC对话, {'模型': self.model, 'id': self.npc_id, '名称': self.name, '对话': cont, '选项': op}]
        GL.DIALOGUE_HISTORY[pid] = send_data
        sk = GL.SOCKETS[pid]
        send(sk, send_data)

npc = NPCX()
