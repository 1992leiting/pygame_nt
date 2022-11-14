
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 120804
        self.name = '神机道人'
        self.title = '祈福'
        self.model = '道士'
        self.mx, self.my = 77.0, 19.0
        self.direction = 1
        self.map_id = 1208
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '看这位少侠气色红润，不如在老服这求上一签？看看运势！我这里的还有祈福石，老夫无法推断之事，少侠可提笔石上，心诚则灵，必有上天庇佑！(祈福可以增加宝宝顶书和炼妖多技能几率)'
                ],
            'options':
            [
                '我要祈福(消耗200仙玉)','我要祈福(消耗5千万银子)','我没什么想选的'
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
