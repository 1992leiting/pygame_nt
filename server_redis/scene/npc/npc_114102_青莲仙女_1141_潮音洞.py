
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114102
        self.name = '青莲仙女'
        self.title = ''
        self.model = '小花'
        self.mx, self.my = 25.0, 33.0
        self.direction = 0
        self.map_id = 1141
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '普陀山是观音姐姐清修之地，紫气蒸腾，烟围雾笼，景色可是十分奇秀','大慈与一切众生乐，大悲与一切众生苦','很多怪病奇毒只有仙家灵丹可以医治','欲朝普陀山，必度莲花池，穿过前面的莲池，便可见到观音姐姐了。'
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
