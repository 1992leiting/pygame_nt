
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150901
        self.name = '商人的鬼魂'
        self.title = ''
        self.model = '野鬼'
        self.mx, self.my = 24.0, 24.0
        self.direction = 2
        self.map_id = 1509
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '哇，这艘船沉了多少年了，想不到还有人能找来','我要投胎……,你问我为什么不走，不，我要守着这艘船，舱里还有我花大价钱买进的珠宝，那才是我的命啊','别看这沉船黑咕隆咚，各种珍奇宝贝可不少。'
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
