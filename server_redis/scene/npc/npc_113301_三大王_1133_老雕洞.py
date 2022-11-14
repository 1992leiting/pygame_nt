
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 113301
        self.name = '三大王'
        self.title = ''
        self.model = '三大王'
        self.mx, self.my = 20.0, 17.0
        self.direction = 1
        self.map_id = 1133
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '听说佛祖挑选的天命取经人其中有一个是金蝉子转世，吃他一块肉能长生不老，真想尝尝啊','近来好象又招收了不少门徒，看来得扩充山头了','狮驼岭的武功博大精深，不是一两天就能领悟的，想要出人头地还需用心苦练','鹰击长空，能破敌军六将，狮驼弟子务必好好修习！'
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
