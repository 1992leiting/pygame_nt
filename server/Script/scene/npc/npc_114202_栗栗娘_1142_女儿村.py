
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114202
        self.name = '栗栗娘'
        self.title = ''
        self.model = '王大嫂'
        self.mx, self.my = 102.0, 56.0
        self.direction = 0
        self.map_id = 1142
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '女儿村的姑娘们个个能歌善舞，我家女儿也一定要好好学学','最近村子里不太平啊，好多姑娘失踪，我女儿前天也不见了，真是急死了','女儿村的姑娘们个个生的俊俏，看着就让人喜爱啊','我的女儿是我唯一的依靠，我就盼着她能平平安安的生活，以后嫁个好人家。'
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
