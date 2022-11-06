
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 82
        self.name = '大力神灵'
        self.title = ''
        self.model = '风伯'
        self.mx, self.my = 27.0, 37.0
        self.direction = 0
        self.map_id = 7082
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你还不知道么?是西海龙王敖闰之白龙三太子，性狂纵火烧了玉帝亲赐的明珠，犯了诛灭九族的大罪，他父王为保宗室，无奈表奏天庭告子忤逆玉帝圣谕先重责三百，然后推上剐龙台挨刀!现在多半关在天牢里叫屈哭冤。'
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
