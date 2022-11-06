
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111201
        self.name = '杨戬'
        self.title = '降妖伏魔'
        self.model = '二郎神'
        self.mx, self.my = 54.5, 53.4
        self.direction = 0
        self.map_id = 1112
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '下界有妖魔作乱，要多加防范才是','不知道嫦娥仙子如何喜欢我，唉，真是苦恼啊#14,天庭也非清净之地，啥时能再回到我的灌江口？,我就是英俊潇洒玉树临风天庭第一美男子二郎神#17'
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
