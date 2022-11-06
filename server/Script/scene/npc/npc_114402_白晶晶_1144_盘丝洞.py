
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114402
        self.name = '白晶晶'
        self.title = '门派师傅'
        self.model = '白晶晶'
        self.mx, self.my = 32.0, 14.0
        self.direction = 1
        self.map_id = 1144
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '盘丝岭从不相信眼泪','师姐一直好像有什么心事','师妹对那个臭猴子还是念念不忘','要想在魔界扬名，还要多加历练才是啊','学本领要虚心，不可轻浮自满','今晚的月亮好亮，不知那猴子身在何处，可有想我？,这里就是当年盘丝大仙修炼的地方。'
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
