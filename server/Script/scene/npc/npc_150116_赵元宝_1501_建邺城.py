
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150116
        self.name = '赵元宝'
        self.title = ''
        self.model = '文老伯'
        self.mx, self.my = 227.0, 79.0
        self.direction = 0
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '建邺虽然小，可是什么都不缺','前几天去了趟长安城，城里的过往客商可真多','建邺的风景还不错吧','老孙头最近好象有什么心事的样子，整天皱着个眉头在自言自语','俗话说无奸不商，如今像我这样清白做生意的商人可真是少见了啊#17,建邺城可谓麻雀虽小，五脏俱全。长安城有的，你在这都能找到#43'
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
