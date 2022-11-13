
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150301
        self.name = '服装店老板'
        self.title = ''
        self.model = '服装店老板'
        self.mx, self.my = 18.0, 19.0
        self.direction = 1
        self.map_id = 1503
        self.npc_type = '商店'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '小店的服饰都是请城里的裁缝精心裁剪的，做工绝对没有问题','城里的老少都穿我卖的衣服','小店布匹又快用光了，过两天得去城里进货','本店服装纯手工制作，随便看看吧。'
                ],
            'options':
            [
                '购买','我只是来看看'
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
