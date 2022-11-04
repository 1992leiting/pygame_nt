
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111401
        self.name = '吴刚'
        self.title = '飞升使者'
        self.model = '大生'
        self.mx, self.my = 26.0, 12.0
        self.direction = 0
        self.map_id = 1114
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '目前来说，以你的修为已经到头了，如果想百尺竿头，更上一步的话，除非能入于化境！'
                ],
            'options':
            [
                '什么是化境','我想入化境，请指点一二。','入化境后有什么变化？','我已经通过考验，请带我入与化境。','我点错了'
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
