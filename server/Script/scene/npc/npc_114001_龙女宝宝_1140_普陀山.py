
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114001
        self.name = '龙女宝宝'
        self.title = ''
        self.model = '小龙女'
        self.mx, self.my = 21.0, 32.0
        self.direction = 0
        self.map_id = 1140
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这里就是普陀山紫竹林了','你也是来拜见大慈大悲观世音菩萨的吗？#18,菩萨最近正在招收徒，只有女性的仙族才收哦#0,元宵节要到了，谁能陪我去长安城观灯？,紫竹林风光无限好，我再也不愿回到水晶宫了。'
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
