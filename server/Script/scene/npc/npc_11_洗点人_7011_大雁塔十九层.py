
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 11
        self.name = '洗点人'
        self.title = ''
        self.model = '道士'
        self.mx, self.my = 463.5, 239.0
        self.direction = 1
        self.map_id = 7011
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我可以帮你的角色进行洗点一次，你确定吗？（洗点将初始化所有点数，并返回潜力值，需要100万银子）'
                ],
            'options':
            [
                '是的我要为角色洗点一次','不了不了'
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
