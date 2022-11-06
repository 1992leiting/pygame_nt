
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 181502
        self.name = '黄色机关人'
        self.title = ''
        self.model = '帮派机关人'
        self.mx, self.my = 23.0, 28.0
        self.direction = 1
        self.map_id = 1815
        self.npc_type = '传送'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我是本帮的机关人，请问你需要进行什么操作？'
                ],
            'options':
            [
                '送我去聚义厅','送我去书院','送我去金库','送我去厢房','送我去兽室','送我去仓库','送我去长安城','我是来破坏你的','取消'
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
