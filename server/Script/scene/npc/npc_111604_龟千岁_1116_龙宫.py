
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111604
        self.name = '龟千岁'
        self.title = ''
        self.model = '龟丞相'
        self.mx, self.my = 99.0, 57.0
        self.direction = 0
        self.map_id = 1116
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '大家叫我龟千岁，可我看起来还是那么年轻吧？,在海里呆得久了，想到陆地上走走','龙族的法术玄妙无比，要苦心修习方能领悟','龙宫里有数不尽的宝贝，有机缘之人才能得到','生蚝肉怎么这么好吃#89,年纪越大，越容易犯低级错误#76'
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
