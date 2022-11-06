
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 113401
        self.name = '大大王'
        self.title = '门派师傅'
        self.model = '大大王'
        self.mx, self.my = 29.0, 18.0
        self.direction = 0
        self.map_id = 1134
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我们这里神仙都不敢来的','最近来投靠的人越来越多，得想法子扩大山头了','学本领要专一，不能三心二意','要想在魔界扬名，还要多下苦功夫才行#2,人不可貌相。别看我的弟子们相貌不够英俊，他们可都是温柔贴贴的好男人呢','要做得山大王，空有一身蛮力是不够的。'
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
