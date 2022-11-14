
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114701
        self.name = '镇元子'
        self.title = '门派师傅'
        self.model = '镇元子'
        self.mx, self.my = 28.0, 20.0
        self.direction = 1
        self.map_id = 1147
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '学了本领要用在正途，不许恃强凌弱','修行要注重基础，持之以恒，切忌好高骛远','想成为仙界的精英，还要下一番苦功夫啊～,我观中的人参果树乃是混沌初分，鸿蒙初判，天地未开之际产成的灵根','师傅领进门，修行在个人。本门法术之精妙还望各位多多领悟。'
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
