
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 112201
        self.name = '钟馗'
        self.title = '钟馗'
        self.model = '钟馗'
        self.mx, self.my = 65.0, 70.0
        self.direction = 1
        self.map_id = 1122
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '最近地府经常有恶鬼出逃，要想想办法才是','我虽然擅长捉鬼，无奈现在散落在外的游魂野鬼实在是太多了……,为人不做亏心事，夜半不怕鬼叫门','我乃赐福镇宅圣君，誓为三界除尽天下之鬼怪妖孽','你可知道我生前是如何死的么？'
                ],
            'options':
            [
                '我来帮你抓鬼','取消任务','我是路过的'
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
