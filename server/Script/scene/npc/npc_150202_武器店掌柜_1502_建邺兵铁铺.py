
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150202
        self.name = '武器店掌柜'
        self.title = ''
        self.model = '马货商'
        self.mx, self.my = 15.0, 18.0
        self.direction = 0
        self.map_id = 1502
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '长安武器店专卖0级和20级武器，0级和10级的武器则在建邺城出售。少侠记住了没#1,瞧一瞧看一看了，我这里的武器最适合新人使用了。边上的老板出售高级一点的兵器，购买时请看清楚物品等级，别买错了哦#2'
                ],
            'options':
            [
                '购买','我只是来看看'
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
