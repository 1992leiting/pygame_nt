
from Script.scene.scene_handler import NPC, scene_transfer
from Common.constants import GL
from Common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 150107
        self.name = '王大嫂'
        self.title = ''
        self.model = '王大嫂'
        self.mx, self.my = 141.0, 12.0
        self.direction = 1
        self.map_id = 1501
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '城北的海岸常有大风浪，岸边那艘沉船，也不知道是哪个年月遇到大风浪沉在那里的,我丈夫出海死了，现在我也只好出来摆摊赚钱养活我那个两个孩子,飞儿可真是个懂事的孩子，年纪轻轻就挑起了全家的重担','瞧一瞧！看一看！新鲜出炉的烤鸭！#51,听过京城的人说，城里到处是亭台楼阁，红砖绿瓦，连皇上都住在那儿，真想去见识一下,在我这里你可以学习烤鸭技巧，学会如何烹饪烤鸭之后你购买一只未煮熟的烤鸭，进行烹饪，烹饪之后的烤鸭不仅可以食用还可以500两银子出售给我,无鸭不成席。来到建邺，你可一定得尝尝我家的烤鸭！'
                ],
            'options':
            [
                ''
                ]
        }

    def talk(self, pid, option=None):
        """
        NPC对话
        :param pid: 玩家id
        :param option: 对话选项
        """
        cont = random.sample(self.dialogue['contents'], 1)
        op = self.dialogue['options']

        if option is not None:
            return

        send_data = [S_发送NPC对话, {'模型': self.model, 'id': self.npc_id, '名称': self.name, '对话': cont, '选项': op}]
        GL.DIALOGUE_HISTORY[pid] = send_data
        sk = GL.SOCKETS[pid]
        send(sk, send_data)

npc = NPCX()
