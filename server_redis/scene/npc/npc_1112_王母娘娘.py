
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111204
        self.name = '王母娘娘'
        self.title = ''
        self.model = '王母'
        self.mx, self.my = 35.0, 31.5
        self.direction = 0
        self.map_id = 1112
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我蟠桃园里的桃子可都是稀世珍品','谁这么大胆，偷走了我的九叶灵芝草#51,蟠桃园的桃子长势喜人，今年又可以开一场盛大的蟠桃宴会了','猴子被佛祖降服以后，天界的日子总算太平了','仙魔两界向来水火不容，说什么神仙妖魔自由恋爱，哼，除非神仙都死光了。'
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
