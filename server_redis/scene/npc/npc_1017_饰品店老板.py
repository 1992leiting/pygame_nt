
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 101701
        self.name = '饰品店老板'
        self.title = ''
        self.model = '赵姨娘'
        self.mx, self.my = 20.0, 18.0
        self.direction = 0
        self.map_id = 1017
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这里出售的都是上等货色，主要是项链腰带一类。客官想买点什么？,珍珠链，买三条，美过翡翠与玛瑙，锦绣饰品店欢迎你','既然来长安旅游，何不在本店买一件护身符留作纪念？,价格很公道的，随便选几样吧','送些精致饰品给意中人，表示一下心意嘛'
                ],
            'options':
            [
                '购买','我什么都不想做'
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
