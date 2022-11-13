
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 184501
        self.name = '玄武堂总管'
        self.title = ''
        self.model = '兰虎'
        self.mx, self.my = 14.0, 15.0
        self.direction = 0
        self.map_id = 1845
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '安定度是帮派必不可少的，如果安定度过低，可能会导致帮派规模降级甚至解散。你可以在我这里通过完成任务来提升帮派的安定度。'
                ],
            'options':
            [
                '领取任务','取消任务','取消'
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
