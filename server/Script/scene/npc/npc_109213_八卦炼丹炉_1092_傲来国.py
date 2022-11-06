
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 109213
        self.name = '八卦炼丹炉'
        self.title = ''
        self.model = '炼丹炉'
        self.mx, self.my = 119.0, 22.0
        self.direction = 0
        self.map_id = 1092
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '少侠可是想要炼制极品丹药？带上你的东西到我这来炼丹吧！运气好的话你会获得价值不菲的灵丹妙药！'
                ],
            'options':
            [
                '我要炼丹','买点炼丹材料','领取寄存丹药','高级内丹','熔炼高级内丹','我什么都不想做'
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
