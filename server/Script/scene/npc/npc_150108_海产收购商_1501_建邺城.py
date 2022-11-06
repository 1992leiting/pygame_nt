
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150108
        self.name = '海产收购商'
        self.title = ''
        self.model = '捕鱼人'
        self.mx, self.my = 230.0, 14.0
        self.direction = 0
        self.map_id = 1501
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我在收购附近的海产，什么大海龟、巨蛙、海毛虫之类的都收#R/（警告：请将不出售的海产召唤兽设置为参战状态）'
                ],
            'options':
            [
                '我卖大海龟（250两银子/只或者300两储备金/只）给你','我卖巨蛙（350两银子/只或者400两储备金/只）给你','我卖海毛虫（500两银子/只或者600两储备金/只）给你','没什么，我只是看看'
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
