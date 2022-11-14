
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104301
        self.name = '空度禅师'
        self.title = '门派师傅'
        self.model = '空度禅师'
        self.mx, self.my = 17.0, 14.0
        self.direction = 1
        self.map_id = 1043
        self.npc_type = '门派师傅'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我佛门心法只传授诚心向佛之士','学道有成，根本在悟','得即是失，失即是得，世事本是过眼烟云，不必太过看重','人生本在是非场，一生难免会有过。修真正道先修心，悟玄讲道渡世人','救人一命，胜造七级浮屠，这才是化生寺弟子天职所在','出家人要以慈悲为怀，善哉善哉','医生难医命终之人，佛陀难渡无缘的众生。'
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
