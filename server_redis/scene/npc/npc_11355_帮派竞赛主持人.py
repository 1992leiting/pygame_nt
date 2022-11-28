
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 1135501
        self.name = '帮派竞赛主持人'
        self.title = '帮派竞赛'
        self.model = '守门天将'
        self.mx, self.my = 141.0, 8.0
        self.direction = 1
        self.map_id = 11355
        self.npc_type = '传送'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我这里每周日19.30会举报一次帮派比武大赛，19:00停止报名开始分组进入场地准备，可以查看对战表查看分组信息，一帮之主可以为自己的帮派报名参赛，报名帮派将获得参赛资格。'
                ],
            'options':
            [
                '对战表','把我送出场地','我只是来看看'
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
