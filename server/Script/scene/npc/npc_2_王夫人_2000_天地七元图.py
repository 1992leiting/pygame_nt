
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 2
        self.name = '王夫人'
        self.title = ''
        self.model = '王大嫂'
        self.mx, self.my = 387.0, 231.0
        self.direction = 0
        self.map_id = 2000
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我老伴早年就去世了，我只剩刘洪这么一个儿子可以依靠了','自从多年前他把我接过来这里享福的时候，我就发现我儿子变了，变的不认识了','我儿子手下的人怎么都叫他陈大人啊#55/,如今虽然吃穿不愁，可是我还总觉得心里不踏实，这是何故?'
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
