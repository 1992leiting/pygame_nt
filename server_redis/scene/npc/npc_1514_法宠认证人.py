
from scene.scene_handler import NPC, scene_transfer
from common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 151401
        self.name = '法宠认证人'
        self.title = '法术认证'
        self.model = '老马猴'
        self.mx, self.my = 37.0, 79.0
        self.direction = 1
        self.map_id = 1514
        self.npc_type = '特殊'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '认证为法宠：雷击、落岩、水攻、烈火、奔雷咒、泰山压顶、水漫金山、地狱烈火、从天而降、月光、八凶法阵、苍鸾怒击、天降灵葫、上古灵符、大快朵颐，龙魂、浮云神马、哼哼哈兮、津津有味、叱咤风云、出其不意、理直气壮、嗜血追击、流沙轻音、食指大动、溜之大吉、神出鬼没、昼伏夜出神兽认证需要8000W。认证费用：参战等级×参战等级×160＋参战等级×4000。认证成功后，其攻击法术即转换成永久携带的“天赋技能”，同时，还会随机获得一个技能使它的技能数量不会减少。'
                ],
            'options':
            [
                '是的我要认证','算了算了'
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
