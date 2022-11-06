
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 109201
        self.name = '渔夫'
        self.title = '钓鱼'
        self.model = '捕鱼人'
        self.mx, self.my = 150.0, 143.0
        self.direction = 0
        self.map_id = 1092
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我这里出售上好的鱼竿，如果打算钓鱼的话就买一根鱼竿去试试身手吧。'
                ],
            'options':
            [
                '花费2000两购买鱼竿','兑换海产','太贵了我没钱'
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
