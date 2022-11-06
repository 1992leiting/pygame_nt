
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 102802
        self.name = '酒店老板'
        self.title = ''
        self.model = '酒店老板'
        self.mx, self.my = 43.0, 26.0
        self.direction = 1
        self.map_id = 1028
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '客官远道而来辛苦了，我们酒店有干净舒适的客房，您休息后可完全回复气血和魔法。休息一次需要500两银子，对于20级以下的玩家，我们不收费'
                ],
            'options':
            [
                '我要住店休息','我精神很好，不想住店'
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
