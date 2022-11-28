
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 107015
        self.name = '强行PK申请人'
        self.title = 'PK开关'
        self.model = '兰虎'
        self.mx, self.my = 45.0, 133.0
        self.direction = 1
        self.map_id = 1070
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '开了pk开关，就可以自由攻击其他玩家了，pk开关最少要在24小时后才可被关闭。当然人气越低将会受到应有的惩罚哦你确认开启吗?'
                ],
            'options':
            [
                '我要打开PK开关','我要关闭PK开关','我就路过看看'
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
