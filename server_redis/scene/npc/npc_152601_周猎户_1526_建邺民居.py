
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 152601
        self.name = '周猎户'
        self.title = ''
        self.model = '兰虎'
        self.mx, self.my = 22.0, 22.0
        self.direction = 1
        self.map_id = 1526
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '最近都打不到什么猎物，日子还怎么过啊，老婆说再这样下去，就得考虑让我进京城打工了','城外的野兽倒不少，可都是凶猛无比，真是恐怖啊','如今外出打猎要带一包袱的草药，都搞不清是谁打谁了','进山不怕虎伤人，下海不怕龙卷身。没有胆量是做不得猎人的','自从建邺城开了新城门，经由我家门口去东海确实方便了许多。'
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
