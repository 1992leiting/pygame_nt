
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 115005
        self.name = '荀卿'
        self.title = '凌波城少主'
        self.model = '剑侠客'
        self.mx, self.my = 49.0, 65.0
        self.direction = 4
        self.map_id = 1150
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '运气到了真是挡都挡不住，居然天上掉金子到我面前','看到借条，想起欠钱不还的张三，这才是睹物思人的最高境界','平顶山上到底埋藏着什么宝贝？#89/,自打朱紫国驿站开通以来，经由郊外去境外的人越来越少了#15'
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
