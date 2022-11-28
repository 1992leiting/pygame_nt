
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 103301
        self.name = '老鸨'
        self.title = ''
        self.model = '红娘'
        self.mx, self.my = 45.0, 38.0
        self.direction = 1
        self.map_id = 1033
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这位大爷，您又来了#1今儿是要小怜香给您唱曲儿还是小惜玉为您跳舞啊？,良辰美景，花好月圆，这位客官喜欢哪位姑娘呀？我这儿的怜香惜玉两位姑娘能歌善舞，您去楼上看看？,我这儿有怜香惜玉两位当红的姑娘，琴棋书画样样都会，您去楼上看看？,这位大爷一看就知道是怜香惜玉之人。我这儿的怜香惜玉两位姑娘能歌善舞，您去楼上看看？,今晚上本楼所有消费一律五折，客官您算是来对了','本楼可是正规娱乐场所#99客官您是要品茶还是饮酒啊？'
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
