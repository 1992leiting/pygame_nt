
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 121601
        self.name = '百兽王'
        self.title = '坐骑任务'
        self.model = '大大王'
        self.mx, self.my = 23.0, 81.0
        self.direction = 0
        self.map_id = 1216
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '等级达到60级可以在我这里花费100体力和200万银子领取坐骑任务，当完成任务可以随机获得一只种族坐骑，成长和属性随机'
                ],
            'options':
            [
                '领取坐骑任务','取消坐骑任务','取消'
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
