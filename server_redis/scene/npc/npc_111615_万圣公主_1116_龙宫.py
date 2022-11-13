
from scene.scene_handler import NPC, scene_transfer

from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111615
        self.name = '万圣公主'
        self.title = ''
        self.model = '万圣公主'
        self.mx, self.my = 18.0, 50.0
        self.direction = 1
        self.map_id = 1116
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '小白龙真是个傻瓜，本公主略施小计就把他整的一点脾气也没有','九头虫怎么还不回来，不知道事情办妥了没有','龙族的法术玄妙无比，要苦心修习方能领悟','龙宫纵有千万般好处，可还是比不上我的乱石山碧波潭。'
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
