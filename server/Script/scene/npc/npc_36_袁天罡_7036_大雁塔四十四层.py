
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 36
        self.name = '袁天罡'
        self.title = ''
        self.model = '诗中仙'
        self.mx, self.my = 357.0, 34.0
        self.direction = 0
        self.map_id = 7036
        self.npc_type = '商店'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你可以在我这里购买灵饰材料，等级≥109级（单人）可以在我这里领取神器任务，领取神器任务需要消耗1万仙玉每人只能获得一个神器'
                ],
            'options':
            [
                '灵宝现世','开启神器·序章','前往剑冢','购买灵饰指南书','购买元灵晶石','神兜兜相关','点错了'
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
