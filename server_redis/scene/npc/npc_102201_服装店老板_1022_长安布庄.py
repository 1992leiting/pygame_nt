
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 102201
        self.name = '服装店老板'
        self.title = ''
        self.model = '服装店老板'
        self.mx, self.my = 32.0, 18.0
        self.direction = 1
        self.map_id = 1022
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '人靠衣装马靠鞍，本店为您提供各种新款服装，就算不买也来看看吧','这里各种绸缎一应俱全，肯定有你想要的。只有大唐官府的玩家才能学会鉴定衣服的技能，而项链腰带的鉴定技能只有地府的玩家才能学','本店的服饰选用的都是上等丝绸布匹，做工细致，包您满意,三分长相，七分打扮，挑件合身的衣服吧。店里的张裁缝可以让你提高裁缝熟练度','要自己做衣服请到那边的裁缝台吧，只收取您少量的加工费。'
                ],
            'options':
            [
                '购买','我只是来看看'
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
