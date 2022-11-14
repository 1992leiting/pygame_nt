
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114204
        self.name = '绿儿'
        self.title = ''
        self.model = '二宝'
        self.mx, self.my = 77.0, 68.0
        self.direction = 1
        self.map_id = 1142
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '上次红线童子送我了个木偶，真好玩，不过只有一个是不是太孤独了。下次再叫他送我个，两个人就不孤独了','你有什么新奇的玩具啊，绿儿一个人好无聊哦','我的意中人是个盖世英雄，他要陪我玩丢手绢，嗯，还要把他的糖糖分给我吃！'
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
