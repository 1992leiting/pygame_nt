
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 48
        self.name = '进阶超级土地公公'
        self.title = ''
        self.model = '进阶超级土地公公'
        self.mx, self.my = 381.0, 60.0
        self.direction = 0
        self.map_id = 7048
        self.npc_type = '神兽'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '商城内可以购买神兽或者使用神兽兜兜可以随机获取一直神兽，神兽可以进阶，进阶后的神兽不但可以改变外形，而且会有特殊的加成哦！'
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
