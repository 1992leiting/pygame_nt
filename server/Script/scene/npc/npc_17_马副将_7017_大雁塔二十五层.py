
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 17
        self.name = '马副将'
        self.title = ''
        self.model = '御林军'
        self.mx, self.my = 193.0, 106.0
        self.direction = 0
        self.map_id = 7017
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '每日玩家可以领取3小时双倍经验，每日中午12点更新双倍时间，更新以后双倍时间不累计叠加'
                ],
            'options':
            [
                '领取一小时双倍经验','领取二小时双倍经验','领取三小时双倍经验','查看剩余的双倍时间','查看队伍双倍时间'
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
