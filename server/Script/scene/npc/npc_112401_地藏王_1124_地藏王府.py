
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 112401
        self.name = '地藏王'
        self.title = '门派师傅'
        self.model = '地藏王'
        self.mx, self.my = 21.0, 21.0
        self.direction = 0
        self.map_id = 1124
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '地狱不空，誓不成佛','修行贵在持之以恒，切忌浮躁自满','地府法术诡异玄妙，只传授有缘之人','地府弟子学有所成是师父我最大的心愿','要想在魔界扬名，还要多加历练才是啊','恶业将盈，地狱相现。'
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
