
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 153701
        self.name = '贸易车队总管'
        self.title = ''
        self.model = '张老财'
        self.mx, self.my = 7.0, 25.0
        self.direction = 1
        self.map_id = 1537
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '别看我官小，建邺城的贸易都是由我掌管的,有钱可以使鬼推磨，恰好我有钱'
                ],
            'options':
            [
                '我要更改造型','我要更改角色的名字','我随便逛逛不好意思'
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
