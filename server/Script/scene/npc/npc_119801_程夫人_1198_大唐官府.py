
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 119801
        self.name = '程夫人'
        self.title = ''
        self.model = '程夫人'
        self.mx, self.my = 28.0, 26.0
        self.direction = 0
        self.map_id = 1198
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我家老程的三板斧据说是在梦中学会的，我才不信呢','现在是太平盛世，百姓安居乐业','我家兄弟当初与老爷并肩作战，现如今也不知身在何处？,听说老爷最近要远征歼杀突厥，真担心他的身子。'
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
