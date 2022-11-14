
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150401
        self.name = '药店老板'
        self.title = ''
        self.model = '药店老板'
        self.mx, self.my = 23.0, 17.0
        self.direction = 1
        self.map_id = 1504
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '城里有位好心的郎中陈长寿，看病从不收银子，他一般都在去东海湾的城门口附近摆摊看病','拉肚子，选好药，选药也要有诀窍','客官需要什么药？,俗话说“对症下药”，这药可是不能乱吃的','佛手可以去长安、西梁女国和朱紫国的药店买哦','药材好，药才好。'
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
