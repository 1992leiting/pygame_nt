
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 105401
        self.name = '程咬金'
        self.title = '门派师傅'
        self.model = '程咬金'
        self.mx, self.my = 17.0, 18.0
        self.direction = 0
        self.map_id = 1054
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '俺的武艺不想带进棺材里，是该找个传人的时候了,一屋不扫何以天下？修身与治国平天下同等重要','俺老程的三板斧可是天下有名的','大唐武艺，天下无双。弟子们江湖行走可别坏了师门的名声,做了官还要天天上朝，真是麻烦','学本领要虚心，可不能浮躁自满','学会俺的一身本领，闯荡江湖绰绰有余。'
                ],
            'options':
            [
                '交谈','给予','师门任务','学习技能'
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
