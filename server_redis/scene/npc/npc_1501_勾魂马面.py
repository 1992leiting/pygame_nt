
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150106
        self.name = '勾魂马面'
        self.title = ''
        self.model = '马面'
        self.mx, self.my = 101.0, 12.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我的工作就是收取厌倦尘世生活的玩家性命，如果你不再留恋这个美好的世界，你的一切都将在我这里终结，请认真做出你的选择，你的朋友、亲人将再也见不到你，你永远只存在他们的记忆当中'
                ],
            'options':
            [
                '我已经想清楚了','我保留意见'
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
