
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 70
        self.name = '大雁塔传送使者'
        self.title = '勇闯大雁塔'
        self.model = '御林军'
        self.mx, self.my = 452.0, 38.0
        self.direction = 1
        self.map_id = 7092
        self.npc_type = '传送'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你可以在我这里直接飞大雁塔，每次飞行需要消耗层数*1万的银子'
                ],
            'options':
            [
                '我要扫荡大雁塔','带我冲上云霄','我要考虑一下'
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
