
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 151305
        self.name = '看门小妖'
        self.title = ''
        self.model = '树怪'
        self.mx, self.my = 185.0, 36.0
        self.direction = 1
        self.map_id = 1513
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我们洞主就是人称魔界一枝花的性感又感性的美女～春十三娘,最近总在附近发现一些人类的骸骨，不知道又是谁吃东西没清理好','金姑娘就喜欢在亭子那里用餐，说是那里风景好，吃东西就吃东西，还用选什么风景','想拜见我们洞主么？找我就对了','盘丝岭的夕阳远望可谓梦幻中最美的风景。'
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
