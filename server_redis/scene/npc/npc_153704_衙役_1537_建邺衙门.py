
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 153704
        self.name = '衙役'
        self.title = ''
        self.model = '衙役'
        self.mx, self.my = 28.0, 28.0
        self.direction = 2
        self.map_id = 1537
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '公堂禁地，闲杂人等不许乱闯','告状的话先把状纸准备好了到堂外排队去，别乱闯','作奸犯科可是要下大狱的','最近大唐国境总有强盗山贼出没，衙门里人手快不够用了','虽有石狮把门，安全还得靠人。'
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
