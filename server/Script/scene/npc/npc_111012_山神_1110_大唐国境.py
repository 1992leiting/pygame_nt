
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111012
        self.name = '山神'
        self.title = ''
        self.model = '雨师'
        self.mx, self.my = 41.0, 239.0
        self.direction = 0
        self.map_id = 1110
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这大唐国境是我的一方地盘，你可不要瞎捣乱。'
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
