
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 61
        self.name = '陈员外'
        self.title = ''
        self.model = '商会总管'
        self.mx, self.my = 164.0, 244.0
        self.direction = 3
        self.map_id = 7061
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '现在是太平盛世，来往客商越来越多，京城也越发的热闹了。你也来做生意的吗，开点的话可以找当铺门口的商会总管申请','不知道如何赚钱吗？找花香香做做赏金任务或者王夫人的新手任务能帮助你赚到长安的第一桶金。想开点的话可以找当铺门口的商会总管申请。'
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
