
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 1
        self.name = '长安导游'
        self.title = ''
        self.model = '书生'
        self.mx, self.my = 463.0, 262.0
        self.direction = 0
        self.map_id = 2000
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '听人说大唐官府的程咬金将军在广招徒弟，不知道谁能有幸拜在他的门下。大唐官府的入口在长安天台的后面','化生寺的空度禅师也在招收徒弟，有兴趣的可以去试试。化生寺的入口在长安大雁塔后面','秦琼将军掌管着点卡寄售处，如有需要随时可以去秦府后院看看#40'
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
