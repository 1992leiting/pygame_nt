
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 54
        self.name = '修炼大师'
        self.title = '修炼提升'
        self.model = '兰虎'
        self.mx, self.my = 248.0, 162.0
        self.direction = 1
        self.map_id = 7054
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '你可以在我这里查看以及设置人物修炼。你还可以在我这里提升人物修炼经验，但是需要消耗一定数量的银子与人物经验。您当前设置的人物修炼类型为：#G/..玩家数据[id].角色.人物修炼.当前..修炼'
                ],
            'options':
            [
                '查看人物修炼信息','设置人物修炼类型','取消'
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
