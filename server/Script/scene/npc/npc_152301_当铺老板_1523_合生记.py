
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 152301
        self.name = '当铺老板'
        self.title = ''
        self.model = '特产商人'
        self.mx, self.my = 25.0, 23.0
        self.direction = 1
        self.map_id = 1523
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你要把物品典当给我吗？如果是#Y/古董#W/的话我的出价会高些，但是如果是普通的物品那么典当价格为正常价格的30%'
                ],
            'options':
            [
                '我有物品需要典当','我只是随便逛逛打扰了'
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
