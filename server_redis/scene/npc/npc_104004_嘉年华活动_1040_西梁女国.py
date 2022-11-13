
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104004
        self.name = '嘉年华活动'
        self.title = ''
        self.model = '嘉年华'
        self.mx, self.my = 87.0, 63.0
        self.direction = 0
        self.map_id = 1040
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你可以在我这里领取嘉年华任务，完成任务后将获得丰厚奖励噢。本任务为环式任务，越到后面奖励越高。'
                ],
            'options':
            [
                '领取任务','取消任务','我是路过的'
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
