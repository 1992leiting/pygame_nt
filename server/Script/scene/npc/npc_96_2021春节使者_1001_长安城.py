
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 96
        self.name = '2021春节使者'
        self.title = '新年快乐'
        self.model = '进阶超级神牛'
        self.mx, self.my = 228.0, 159.0
        self.direction = 1
        self.map_id = 1001
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你可以在我这里领取春节任务，新年积分可以抽奖，也可以选择去昆仑仙境挂机获得经验，每隔60秒会自动获得经验奖励(需要购买道具)'
                ],
            'options':
            [
                '领取新年任务','领取新年单人任务','取消新年任务','取消新年单人任务','我要去昆仑仙境','我要购买挂机物品','我要抽奖(消耗新年积分)','我要查看新年积分','随便看看'
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
