
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 100902
        self.name = '镇塔之神'
        self.title = ''
        self.model = '渡劫神天兵'
        self.mx, self.my = 24.0, 39.0
        self.direction = 0
        self.map_id = 1009
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '下了场血雨， 阵腥风过后大雁塔的镇塔之宝定魂珠就不见了。大塔镇压十万妖魔，从来没有出过这样的大事，现在塔中妖魔蠢蠢欲动若让他们逃逸四方，天下就要大乱了!'
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
