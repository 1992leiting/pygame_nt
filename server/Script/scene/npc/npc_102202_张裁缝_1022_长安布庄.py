
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 102202
        self.name = '张裁缝'
        self.title = ''
        self.model = '服装店老板'
        self.mx, self.my = 10.0, 23.0
        self.direction = 3
        self.map_id = 1022
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我裁剪的衣服，穿过的人没有说不好的！我一眼看过去，不用尺，就知道你的三围是多少！'
                ],
            'options':
            [
                '咨询打造方法','有什么需要帮忙的（打工增加熟练度）','查看熟练度','我只是随便看看'
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
