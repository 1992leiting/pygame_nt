
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 27
        self.name = '御林军左统领'
        self.title = '皇宫飞贼'
        self.model = '御林军'
        self.mx, self.my = 99.0, 53.0
        self.direction = 0
        self.map_id = 7027
        self.npc_type = '任务'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '整个皇宫的安危就靠我一个人管理，你说我牛逼不？飞贼活动在12点开始，请留心关注系统公告'
                ],
            'options':
            [
                '协助抓捕盗贼','取消任务','我是路过打酱油的'
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
