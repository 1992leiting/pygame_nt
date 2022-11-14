
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 100
        self.name = '元神使徒'
        self.title = '蚩尤元神'
        self.model = '进阶狂豹人形'
        self.mx, self.my = 252.0, 113.0
        self.direction = 1
        self.map_id = 7010
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '最近地府经常有恶鬼出逃，要想想办法才是','我虽然擅长捉鬼，无奈现在散落在外的游魂野鬼实在是太多了……,为人不做亏心事，夜半不怕鬼叫门','我乃赐福镇宅圣君，誓为三界除尽天下之鬼怪妖孽','你可知道我生前是如何死的么？'
                ],
            'options':
            [
                '我要领取元神任务','我想查看我的元神层数','我要提升元神境界(需战斗)','我来看看'
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
