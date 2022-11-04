
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 81
        self.name = '商人鬼魂剧情'
        self.title = '新手剧情'
        self.model = '野鬼'
        self.mx, self.my = 37.0, 21.0
        self.direction = 0
        self.map_id = 7081
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '故事发生在风景秀丽的建邺小城，你在城中闲逛的时候遇到了愁眉苦脸的老孙头，询问之后得知老人的心事，于是你答应帮他找法师超度死去的渔民。'
                ],
            'options':
            [
                '领取商人的鬼魂','取消商人的鬼魂'
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
