
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 69
        self.name = '帮派竞赛主持人'
        self.title = '帮派竞赛'
        self.model = '守门天将'
        self.mx, self.my = 378.0, 160.0
        self.direction = 1
        self.map_id = 7069
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我这里每周日19.30会举报一次帮派比武大赛，19:00停止报名开始分组进入场地准备，可以查看对战表查看分组信息，一帮之主可以为自己的帮派报名参赛，报名帮派将获得参赛资格。'
                ],
            'options':
            [
                '我要报名参赛','送我去比赛场地','对战表','我要进入帮派迷宫','我要进入场地领取宝箱','我只是来看看'
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
