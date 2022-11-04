
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114203
        self.name = '柳飞絮'
        self.title = ''
        self.model = '小花'
        self.mx, self.my = 23.0, 88.0
        self.direction = 0
        self.map_id = 1142
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '青琉璃女侠是我的恩人，我一直在想着报答她','最近村子里失踪了好几个姑娘，家里人都担心死了，特别是那个栗栗儿的娘，天天在村子附近寻找女儿，真是作孽啊','婆婆传授的法术是用来防身用的，可不是用来逞强的。'
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
