
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150124
        self.name = '管家'
        self.title = ''
        self.model = '小二'
        self.mx, self.my = 34.0, 57.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '这是李老爷的府上，在这个小城里，我们老爷可是知名度最高的人了','我家老爷最近病的厉害，医生怎么查也查不出是什么原因','当个管家也不容易呀，每天忙里忙外，什么杂七杂八的事情都得打点','人说做一次善事容易，做一辈子善事就难咯，在这点上我是万分钦佩我家老爷的','建邺城啥时才能开个长安城那样的赌坊呢#80'
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
