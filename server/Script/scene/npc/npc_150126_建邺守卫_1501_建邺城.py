
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150126
        self.name = '建邺守卫'
        self.title = '传送江南野外'
        self.model = '衙役'
        self.mx, self.my = 15.5, 138.5
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '传送'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '天天在这边看门真是没意思，我也渴望刺激的生活','前面就是江南野外了，没有实力可不要硬闯，小心被野兽吃的骨头都不剩！'
                ],
            'options':
            [
                '传送江南野外','我只是路过'
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
