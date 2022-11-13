
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 12
        self.name = '门派传送人'
        self.title = ''
        self.model = '郑镖头'
        self.mx, self.my = 478.0, 246.8
        self.direction = 1
        self.map_id = 7012
        self.npc_type = '门派传送'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '少侠请选择要为你传送的门派'
                ],
            'options':
            [
                '方寸山','女儿村','神木林','化生寺','大唐官府','盘丝洞','阴曹地府','无底洞','魔王寨','狮驼岭','天宫','普陀山','凌波城','五庄观','龙宫','花果山','天机城','女魃墓'
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
