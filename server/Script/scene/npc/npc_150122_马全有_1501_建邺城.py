
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150122
        self.name = '马全有'
        self.title = ''
        self.model = '武器店老板'
        self.mx, self.my = 49.0, 95.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '听说这里有动物的毛能治小儿惊风，此次我是特地来这收购货物的','我是专门走南闯北倒卖货物的商人','求老天保佑，早日除去城外的野兽，免得我们出城还要提心吊胆','衙门里的简师爷平日深居简出，低调得很','您要点什么，下次我给您带来','衙天南地北的特产我这都有，就连地府的东西我也能搞到。'
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
