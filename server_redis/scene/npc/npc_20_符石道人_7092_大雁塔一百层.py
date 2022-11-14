
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 20
        self.name = '符石道人'
        self.title = '符石开孔'
        self.model = '道童'
        self.mx, self.my = 488.0, 201.0
        self.direction = 1
        self.map_id = 7092
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '装备需要通过开运增加开运孔数才能进行符石镶嵌，而点化此乃上古秘传道术。贫道近期正修炼此法，你有兴趣的话可以来试试。'
                ],
            'options':
            [
                '我来给装备开运','点化装备星位','我来合成符石','我可不想给装备开运'
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
