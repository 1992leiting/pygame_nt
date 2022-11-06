
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 15
        self.name = '皇宫护卫'
        self.title = '平定安邦'
        self.model = '御林军'
        self.mx, self.my = 210.0, 98.0
        self.direction = 0
        self.map_id = 7015
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '玩家在对应的野外场景战斗时，将会获得心魔宝珠。集齐20颗心魔宝珠后可以来我这里换取奖励。'
                ],
            'options':
            [
                '领取平定安邦任务','我来取消任务','上交心魔宝珠','我马上去搜集'
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
