
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114401
        self.name = '春十三娘'
        self.title = ''
        self.model = '春十三娘'
        self.mx, self.my = 28.0, 39.0
        self.direction = 1
        self.map_id = 1144
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '桃花过处，寸草不生。很多年之后，我有个绰号，叫做桃花娘子……,我有一项不传绝技，叫作“催情大法”','师妹对那个臭猴子还是念念不忘','在出道的时候，我认识一个人，他叫孙悟空，他后来有个绰号，叫齐天大圣','我盘丝洞的法术可不是轻易能学到手的','现在的孙猴子早就不是五百年前那个孙猴子了','往前算五百年，往后算五百年，没人的美貌能超越我#99'
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
