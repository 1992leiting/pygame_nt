
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 107016
        self.name = '马婆婆'
        self.title = '孩子系统'
        self.model = '老太婆'
        self.mx, self.my = 52.0, 147.0
        self.direction = 1
        self.map_id = 1070
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '有自己的可爱宝宝真是一件开心的事呀，如果你想领养小孩，那来找我就对了。拜完门派在原有技能上加门派法术，其他技能随机顶技能。一共有4种法术可以供孩子学习1.门派法术2.六艺法术3.兽决4.物品(比如还魂秘术)'
                ],
            'options':
            [
                '我要收养孩子','领取逍遥镜','关于六艺修行','关于门派法术','关于孩子进阶','设置孩子成长方向','孩子饰品','重置孩子属性','我就路过看看'
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
