
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 121602
        self.name = '仙缘染坊主'
        self.title = '坐骑染色'
        self.model = '赵姨娘'
        self.mx, self.my = 120.0, 61.0
        self.direction = 1
        self.map_id = 1216
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '“凡染，春暴练，夏綞玄，秋染夏，冬秋功。掌凡染事。”人界皆有染色之业，桃源也不例外。只要你有足够的材料，你可以在我这里变换坐骑肤色以及坐骑装饰品颜色。要不要来，染染看#89/'
                ],
            'options':
            [
                '啊！太好了!我正好想换换我的坐骑颜色','我要更换饰品的颜色','我悄悄的走，不带走一片云彩。'
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
