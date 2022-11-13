
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 153706
        self.name = '简师爷'
        self.title = ''
        self.model = '罗师爷'
        self.mx, self.my = 43.0, 17.0
        self.direction = 1
        self.map_id = 1537
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这日子有点太平过头了，半个月来一个告状的都没有','我们建邺城北门附近，有个有名的郎中叫陈长寿，他可以帮新朋友进行免费治疗','我们这里可是清水衙门，不收礼的','作奸犯科之事，衙门绝不会放过','清廉方正，一心为民，为官之道也。'
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
