
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 32
        self.name = '帮派总管'
        self.title = ''
        self.model = '蒋大全'
        self.mx, self.my = 388.0, 13.0
        self.direction = 0
        self.map_id = 7032
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '人在江湖飘哪能不挨刀。少侠赶紧在我这里加入一个帮派吧，有帮派罩着你走路都可以躺着走哟。'
                ],
            'options':
            [
                '加入帮派','送我回帮','创建帮派','取消'
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
