
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 107002
        self.name = '陆萧然'
        self.title = '任务链'
        self.model = '老书生'
        self.mx, self.my = 20.0, 185.0
        self.direction = 0
        self.map_id = 1070
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你可以在我这里领取任务链，任务链由150个小任务组成。每个小任务必须在60分钟内完成。完成本任务后可获得高级书铁以及大量经验奖励。领取本任务需要消耗#G/角色等级*角色等级*20#W/两银子，且角色等级必须达到60级。'
                ],
            'options':
            [
                '我来领取任务链任务','我来取消任务链任务','跳过任务(消耗银子)','我什么都不想做'
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
