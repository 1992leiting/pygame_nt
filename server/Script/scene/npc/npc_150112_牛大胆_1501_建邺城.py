
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150112
        self.name = '牛大胆'
        self.title = ''
        self.model = '道士'
        self.mx, self.my = 229.0, 36.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '驱鬼除妖测字算命啦，前算五百年，后算五百年','这位朋友面带福相，印堂发亮，想是遇到什么喜事了吧','我就是英俊潇洒玉树临风嫉恶如仇斩妖除魔的方寸第一道士牛大胆！#51,城里的渔夫出海打渔之前，都爱到我这里算上一卦','求神问卦，看人说话。这位你可要来让我瞧瞧？'
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
