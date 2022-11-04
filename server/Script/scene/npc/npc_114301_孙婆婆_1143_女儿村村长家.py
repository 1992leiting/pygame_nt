
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114301
        self.name = '孙婆婆'
        self.title = '门派师傅'
        self.model = '孙婆婆'
        self.mx, self.my = 25.0, 20.0
        self.direction = 0
        self.map_id = 1143
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我女儿村的技能只适合女弟子学习','不知道有多少弟子掌握了制出淬毒暗器的秘法？,前几天教了村里的姑娘们一套法术，不知道修习的如何了','村里人口虽然不多，却个个都是貌美如花的绝世高手','修习贵在持之以恒，专心如始方能有所领悟。'
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
