
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150606
        self.name = '楚恋依'
        self.title = ''
        self.model = '小花'
        self.mx, self.my = 57.0, 37.0
        self.direction = 0
        self.map_id = 1506
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '从这里过去可以到建邺，那里的风景很不错的','东海湾常有怪物出没，可要小心','长安城里的集市很热闹的，有机会一定要去看看','东海边的林老汉可以带你去东海岩洞，那里能遇到海毛虫哦#40,东海之水，载不动我沉沉的依恋。'
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
