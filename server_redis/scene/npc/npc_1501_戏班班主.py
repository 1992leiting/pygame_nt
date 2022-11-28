
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150102
        self.name = '戏班班主'
        self.title = ''
        self.model = '文老伯'
        self.mx, self.my = 87.0, 29.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '好消息！最近老夫请到了京城梨园的名角来献艺，机会难得，各位千万不要错过了','听戏可是人生的一大乐趣啊~#51,我们是远近闻名的草台班子，南腔北调昆腔越剧流行歌曲你想听什么都有,真是太平盛世啊，老百姓衣食无忧，闲暇时间还是多听听戏吧','一到戏台开演的日子，建邺城总是万人空巷。'
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
