
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 104403
        self.name = '房玄龄'
        self.title = ''
        self.model = '考官'
        self.mx, self.my = 54.5, 61.0
        self.direction = 3
        self.map_id = 1044
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '我们做臣子的就是要对皇上忠心，为皇上分忧','臣闻理国要道，在于公平正直，故《尚书》云：“无偏无党，王道荡荡。无党无偏，王道平平。”,吃醋吃醋，我的老婆爱吃醋#47/,我自渭北投笔从戎跟随皇上至今，皇上一直待我不薄，我自当鞠躬尽瘁以报答皇上的大恩','别人说我老谋深算，其实我也有单纯的一面#17/'
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
