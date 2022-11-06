
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104404
        self.name = '杜如晦'
        self.title = ''
        self.model = '考官'
        self.mx, self.my = 64.5, 67.0
        self.direction = 3
        self.map_id = 1044
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '在朝为官要尽好自己的本分，对得起圣上和天下百姓','当今圣上治国有方，这是百姓之福','想当年我跟随皇上一起征战四方，那是何等的意气风发。我真是老了，就喜欢怀念过去','唐王昨日梦中被泾河龙王的阴魂所惊吓，今晚我定要守在宫门处保驾','时代不同了，现在大唐弟子都骑上了高头大马，真是比老夫当年的呼雷豹还要威风！'
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
