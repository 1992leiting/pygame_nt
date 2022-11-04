
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111202
        self.name = '李靖'
        self.title = '门派师傅'
        self.model = '李靖'
        self.mx, self.my = 26.0, 43.0
        self.direction = 0
        self.map_id = 1112
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '下界凡间遇到纷争可不要与他们一般见识，他们可是不讲理的','下界有妖魔作乱，要多加防范才是','天庭冷落，真想再回到人间','想成为天界的精英，是要下一番苦功夫的','修行贵在持之以恒，切记浮躁自满。'
                ],
            'options':
            [
                '交谈','给予','师门任务','学习技能'
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
