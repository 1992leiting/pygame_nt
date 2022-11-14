
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150604
        self.name = '捕鱼人'
        self.title = '传送东海岩洞'
        self.model = '捕鱼人'
        self.mx, self.my = 91.0, 81.0
        self.direction = 1
        self.map_id = 1506
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这附近有个岩洞，进去过的人都说里面有很厉害的怪物，最好找一些伙伴一起进去比较安全，你也想进去冒险吗？'
                ],
            'options':
            [
                '是的，我想进去探个究竟','我怕黑，还是不进去了'
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
