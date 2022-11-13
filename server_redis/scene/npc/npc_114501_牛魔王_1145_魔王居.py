
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114501
        self.name = '牛魔王'
        self.title = '门派师傅'
        self.model = '牛魔王'
        self.mx, self.my = 33.0, 21.0
        self.direction = 1
        self.map_id = 1145
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '家家有本难念的经，本王一世英明，如今却家事缠身，可叹啊','你们谁瞧见了本王的避水金睛兽？,学本领要专心，不能三天打渔，两天晒网','想称霸江湖不是那么容易，要专心修行才行。'
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
