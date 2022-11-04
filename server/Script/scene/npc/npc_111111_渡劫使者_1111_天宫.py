
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111111
        self.name = '渡劫使者'
        self.title = '渡劫任务'
        self.model = '进阶蚩尤'
        self.mx, self.my = 18.0, 39.0
        self.direction = 2
        self.map_id = 1111
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '任务领取条件：人物等级达到155级.修炼满25修师门技能165级召唤兽修炼25（猎术不做要求）全修25渡劫上限30修。'
                ],
            'options':
            [
                '我要渡劫','渡劫降修','取消'
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
