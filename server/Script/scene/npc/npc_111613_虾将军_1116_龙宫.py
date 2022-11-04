
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111613
        self.name = '虾将军'
        self.title = ''
        self.model = '虾兵'
        self.mx, self.my = 195.0, 88.0
        self.direction = 0
        self.map_id = 1116
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '有志青年应该投奔我龙宫，及早谋个好前程啊','海底地形复杂，当心可别迷了路','最近宫里丢了颗定颜珠，千岁正发愁呢','论智慧我比蟹将军高那么一点点，可是他比我多了好多手脚，所以比我升的快','八只脚，抬面鼓，两把剪刀鼓前舞，生来横行又霸道，嘴里常把泡沫吐。少侠猜猜是谁？#86,不想当龙虾的虾不是好虾#40'
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
