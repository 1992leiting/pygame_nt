
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 153401
        self.name = '李善人'
        self.title = ''
        self.model = '张老财'
        self.mx, self.my = 14.0, 24.0
        self.direction = 0
        self.map_id = 1534
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '日行一善，积善成德','钱财是身外之物，能用来济世行善是最好不过','老夫虽膝下无子，但这万贯家财我已经找到了继承人','我已经不再年轻了，但我喜欢帮助有志向有作为的年轻人'
                ],
            'options':
            [
                ''
                ]
        }

    def talk(self, pid, content=None, option=None):
        """
        NPC对话
        """
        cont = random.sample(self.dialogue['contents'], 1)
        op = self.dialogue['options']

        if content is not None:
            cont = content
        if option is not None:
            op = option

        send_data = {'模型': self.model, 'npc_id': self.npc_id, '名称': self.name, '对话': cont, '选项': op, '类型': 'npc'}
        send2pid(pid, S_发送NPC对话, send_data)
    
    def response(self, pid, msg):
        pass

npc = NPCX()
