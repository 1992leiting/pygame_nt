
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 122603
        self.name = '古董商人'
        self.title = '黑市竞拍'
        self.model = '钱庄老板'
        self.mx, self.my = 59.0, 96.0
        self.direction = 1
        self.map_id = 1226
        self.npc_type = '商店'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这里还有考古挖掘必备的铁铲出售，挖到好货记得来找我啊!考古其实是一件很有趣的事情，既可以获得经验，而且还有机会赚大钱。要存放古玩的话可以先在我这里买一个收藏柜。'
                ],
            'options':
            [
                '看看你这有什么卖的','参加黑市拍卖会','卖点古玩换钱花','随便看看'
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
