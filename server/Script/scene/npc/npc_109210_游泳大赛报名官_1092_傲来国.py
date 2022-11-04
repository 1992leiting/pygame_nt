
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 109210
        self.name = '游泳大赛报名官'
        self.title = '游泳比赛'
        self.model = '进阶超级海豚'
        self.mx, self.my = 147.0, 62.0
        self.direction = 2
        self.map_id = 1092
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你可以在我这里参加游泳比赛，只要在十五位裁判处完成报道即可获得奖励。每人每日只可以参加两次游泳比赛。本活动全天开放。'
                ],
            'options':
            [
                '我要参赛','我来取消任务','取消'
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
