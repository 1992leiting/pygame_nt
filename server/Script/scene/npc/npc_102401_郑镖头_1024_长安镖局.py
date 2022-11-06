
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 102401
        self.name = '郑镖头'
        self.title = '押镖任务领取人'
        self.model = '郑镖头'
        self.mx, self.my = 32.0, 23.0
        self.direction = 1
        self.map_id = 1024
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '您可以在我这里领取押镖任务。本任务只要领取成功后，将商品运送到指定的NPC后自动完成并获得奖励。'
                ],
            'options':
            [
                '一级镖银(要求等级30、可得25000两银子和50000储备)','二级镖银(要求等级50、可得35000两银子和75000储备)','三级镖银(要求等级70、可得75000两银子和150000储备)','四级镖银(要求等级90、可得110000两银子和225000储备)','五级镖银(要求等级110、可得150000两银子和300000储备)','取消运镖任务','离开'
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
