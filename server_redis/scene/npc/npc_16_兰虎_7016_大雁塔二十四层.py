
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 16
        self.name = '兰虎'
        self.title = '比武大会'
        self.model = '兰虎'
        self.mx, self.my = 428.0, 173.0
        self.direction = 1
        self.map_id = 7016
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '等级达到60级的玩家可以在我这里参加比武大会活动。比武大会活动每日20-21点进行，19点50分-20点为进场时间。比武开始后将无法传送至比武场景内。请选择你要进行的操作：'
                ],
            'options':
            [
                '送我进去','领取奖励','兑换物品','没有什么想玩的'
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
