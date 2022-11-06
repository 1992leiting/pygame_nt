
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 113101
        self.name = '守山小妖'
        self.title = ''
        self.model = '雷鸟人'
        self.mx, self.my = 114.0, 8.0
        self.direction = 1
        self.map_id = 1131
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这里的三位大王各有一手看家本领，说出来怕会吓死你','我家的三个大王分别住在三个山洞里','加入我们狮驼岭，保证你有吃有喝，前途无量','我们狮驼岭的小妖，光是有名有姓的就有四万七八千','我家的三个大王神通广大，就是神仙来也得让着三分。'
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
