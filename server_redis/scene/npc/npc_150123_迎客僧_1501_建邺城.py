
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150123
        self.name = '迎客僧'
        self.title = ''
        self.model = '胖和尚'
        self.mx, self.my = 10.0, 89.0
        self.direction = 0
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '善哉善哉，佛祖有云：“一人出家，全家光荣”，这位施主看似颇有慧根，应该及早皈依我佛门才是啊','不知上次赵捕头有没有记得帮我替我带香烛回来','师傅常说，“心静则万事静，心清则万事清”，我特地到这个清静的小城来体验生活','不要问我从何而来，我站在这就是神仙一样的存在','和尚越老越值钱#18'
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
