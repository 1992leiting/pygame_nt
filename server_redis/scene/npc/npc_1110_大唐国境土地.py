
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 111001
        self.name = '大唐国境土地'
        self.title = '传送凌波城'
        self.model = '土地'
        self.mx, self.my = 177.0, 74.0
        self.direction = 3
        self.map_id = 1110
        self.npc_type = '传送'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '大唐国境之内，鸟语花香，山清水秀，国泰民安，乃是一颇得上天福泽庇佑的所在'
                ],
            'options':
            [
                '送我去凌波城','是吧我也这么觉得'
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
