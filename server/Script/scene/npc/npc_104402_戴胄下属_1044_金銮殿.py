
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104402
        self.name = '戴胄下属'
        self.title = ''
        self.model = '考官'
        self.mx, self.my = 78.5, 57.5
        self.direction = 1
        self.map_id = 1044
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '做官就是舒服，好过平头百姓奔波操劳','善恶到头终有报，我的报应是快到了','俗话说“左眼跳财，右眼跳灾”，为什么我最近老是跳右眼呢，肯定是跳错了','俺老娘也真是的，好吃好喝伺候着，还总是想东想西！'
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
