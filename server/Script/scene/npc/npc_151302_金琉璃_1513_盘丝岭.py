
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 151302
        self.name = '金琉璃'
        self.title = ''
        self.model = '如意仙子'
        self.mx, self.my = 64.5, 81.0
        self.direction = 0
        self.map_id = 1513
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我一直想验证一下，佛光中炼成的宝物，是不是也可以用恶魔之心加以感化呢？,我从何处而生？又要去往何处？,为什么，为什么我总感觉冥冥之中有几个声音在耳边，而那声音又那么象我自己？,什么？你找女儿村的小姑娘？不认识！我从未去过女儿村！！'
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
