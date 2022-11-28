
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111019
        self.name = '长安保卫战使者'
        self.title = ''
        self.model = '御林军'
        self.mx, self.my = 321.0, 193.0
        self.direction = 0
        self.map_id = 1110
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '大唐年间，国富民强，百姓生活幸福。东土的兴盛引起的一些西方妖魔的垂涎，欲进入大唐都城——长安肆虐一番。为了保护长安百姓，唐王请天下英雄协助抵御西方妖魔，有志之士纷纷响应。'
                ],
            'options':
            [
                '我要查看长安保卫战当前积分','我要查看长安保卫战累计积分','我要抽奖(消耗长安保卫战当前积分)','路过的'
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
