
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 76
        self.name = '地载阵守卫1'
        self.title = '阵法挑战'
        self.model = '犀牛将军兽形'
        self.mx, self.my = 84.0, 59.0
        self.direction = 0
        self.map_id = 7076
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '霞影璀璨，虹霓绚烂，彩练仙子以虹光霞影，幻化为诸般阵法，邀三界侠士前来挑战!。'
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
