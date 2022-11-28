
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 151301
        self.name = '女妖'
        self.title = ''
        self.model = '芙蓉仙子'
        self.mx, self.my = 110.0, 104.0
        self.direction = 1
        self.map_id = 1513
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '盘丝洞几百年的规矩，不许男人入住，连收徒也只收女弟子','晶晶姑娘又发脾气了，把犯了门规的小妖挂在洞外七天七夜，差点咽了气','金琉璃最近老带着些人类女孩进进出出的，不知道在搞什么名堂','我已修行了千年，为何还未成仙？,濯垢泉乃天然温泉，是姐妹们美容养颜的好去处#97'
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
