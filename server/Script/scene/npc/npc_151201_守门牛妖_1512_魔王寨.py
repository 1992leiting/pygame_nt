
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 151201
        self.name = '守门牛妖'
        self.title = ''
        self.model = '牛妖'
        self.mx, self.my = 13.0, 75.0
        self.direction = 1
        self.map_id = 1512
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我们寨主就是人称平天大圣的牛魔王','别看齐天大圣厉害，见到我们大王还不一样得叫大哥','我们大王正在和九头虫喝酒呢','加入魔王寨，保你有吃有喝，没人敢再欺负你','自从大王修炼出了五火神焰印，我们寨子一下就人丁兴旺起来了#89'
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
