
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114502
        self.name = '九头精怪'
        self.title = '种族任务'
        self.model = '九头精怪'
        self.mx, self.my = 17.0, 23.0
        self.direction = 0
        self.map_id = 1145
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '别想在我背后做坏事，我有十八只眼睛盯着你呢','只要我成为天命取经人取得真经，将来就能由魔转仙，哈哈哈哈#18,小白龙估计已经被天谴了吧，哈哈哈哈','几天没见万圣公主了，可真想她啊#52'
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
