
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 114201
        self.name = '翠花'
        self.title = ''
        self.model = '翠花'
        self.mx, self.my = 73.0, 96.0
        self.direction = 0
        self.map_id = 1142
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这里的孙婆婆很和蔼的，弟子们有不明白的地方，她总是耐心教导','长安城真的像姑娘们说得那样繁花似锦么？真想哪天去看一看','这里就是远近闻名的女儿村，拜师的话请找孙婆婆','鸳鸯双栖蝶双飞，满眼春色惹人醉。'
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
