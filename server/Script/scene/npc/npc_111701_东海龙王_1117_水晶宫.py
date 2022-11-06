
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111701
        self.name = '东海龙王'
        self.title = '门派师傅'
        self.model = '东海龙王'
        self.mx, self.my = 33.0, 25.0
        self.direction = 1
        self.map_id = 1117
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '龙宫里有数不尽的宝贝，有机缘之人方能得到','龙族的法术玄妙精深，要苦心修习方能领悟','修行贵在用心领悟，切忌轻浮自满','要想成为仙界的精英，是要下一番苦功夫的','遇到大唐弟子可千万别跟他们蛮干，切记','为人间降雨是老夫的职责所在。'
                ],
            'options':
            [
                '交谈','给予','师门任务','学习技能'
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
