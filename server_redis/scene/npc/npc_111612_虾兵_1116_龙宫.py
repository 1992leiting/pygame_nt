
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111612
        self.name = '虾兵'
        self.title = ''
        self.model = '虾兵'
        self.mx, self.my = 188.0, 92.0
        self.direction = 0
        self.map_id = 1116
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '龙宫的宝贝真是多啊，随便偷得一两件拿到外面来卖都能发笔横财','瞧一瞧看一看了，东海龙宫宝贝大展销啦#51,三界之间的恩怨情仇，从来就和我们这种小角色无关#109'
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
