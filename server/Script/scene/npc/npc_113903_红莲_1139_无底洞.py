
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 113903
        self.name = '红莲'
        self.title = ''
        self.model = '修罗傀儡妖'
        self.mx, self.my = 29.0, 15.0
        self.direction = 1
        self.map_id = 1139
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我这么年轻美丽，一定是妹妹啦，你们说对不对#86,你猜墨衣是我的姐姐还是我的妹妹#110,其实我有点害怕姐姐呢，这么多年了，她一直都是那么严厉，比地涌夫人还凶#17'
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
