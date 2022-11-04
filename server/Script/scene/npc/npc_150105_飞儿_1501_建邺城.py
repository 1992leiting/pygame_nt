
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150105
        self.name = '飞儿'
        self.title = ''
        self.model = '飞儿'
        self.mx, self.my = 106.0, 37.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '商店'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '上面粉蒸出来的包子，客官想要几个','建邺虽小，可样样齐全，什么都有#2货栈边上那个王大嫂做的烤鸭真是好吃','包子有肉不在褶上，肚里有货不在嘴上。'
                ],
            'options':
            [
                '购买','我什么也不想做'
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
