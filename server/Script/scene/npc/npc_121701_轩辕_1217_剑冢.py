
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 121701
        self.name = '轩辕'
        self.title = ''
        self.model = '化圣_剑侠客'
        self.mx, self.my = 124.0, 106.0
        self.direction = 1
        self.map_id = 1217
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你没有任务是怎么进来的'
                ],
            'options':
            [
                ''
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
