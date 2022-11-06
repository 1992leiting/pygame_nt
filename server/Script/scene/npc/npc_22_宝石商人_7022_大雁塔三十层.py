
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 22
        self.name = '宝石商人'
        self.title = ''
        self.model = '钱庄老板'
        self.mx, self.my = 496.0, 138.0
        self.direction = 1
        self.map_id = 7022
        self.npc_type = '商店'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我这里暂时不出售任何宝石。但是你可以在我这里使用宝石镶嵌功能。合成宝石只需右击宝石，即可自动合成。合成必须保证你的包裹里有另一颗类型相同且等级相同的宝石才可成功合成。'
                ],
            'options':
            [
                '购买宝石','镶嵌宝石','镶嵌珍珠'
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
