
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 92
        self.name = '风扬阵头领'
        self.title = '阵法挑战'
        self.model = '进阶风伯'
        self.mx, self.my = 106.0, 87.0
        self.direction = 0
        self.map_id = 7092
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '霞影璀璨，虹霓绚烂，彩练仙子以虹光霞影，幻化为诸般阵法，邀三界侠士前来挑战!。'
                ],
            'options':
            [
                '领取风扬阵挑战','取消风扬阵挑战'
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
