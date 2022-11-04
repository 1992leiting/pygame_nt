
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111203
        self.name = '玉皇大帝'
        self.title = ''
        self.model = '玉帝'
        self.mx, self.my = 29.8, 34.8
        self.direction = 0
        self.map_id = 1112
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '作皇帝难，作玉皇大帝更难啊','那个什么九头虫献上的宝贝还真不错','其实我很怕我老婆的，很多事情都是她做主，但是话说回来，怕她，说明我爱她嘛#17你说是不是','汝等不来接受朕的考验，就别想飞升化境#99,那猴子自从跟了唐三藏取经，好久都没消息了，也不知道现在行至何处？'
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
