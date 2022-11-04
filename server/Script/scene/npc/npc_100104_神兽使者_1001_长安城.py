
from Script.scene.scene_handler import NPC, scene_transfer
from Script.common.constants import GL
from Script.common.common import *
import random

class NPCX(NPC):
    def __init__(self) -> None:
        super().__init__()
        self.npc_id = 100104
        self.name = '神兽使者'
        self.title = '灵兜兜兑换'
        self.model = '超级鲲鹏'
        self.mx, self.my = 220.0, 154.0
        self.direction = 0
        self.map_id = 1001
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {
            'contents':
            [
                '北冥有鱼，其名为鲲。鲲之大，不知其几千里也；化而为鸟，其名为鹏。鹏之背，不知其几千里也；怒而飞，其翼若垂天之云。是鸟也，海运则将徙于南冥。南冥者，天池也！#50不错，不错，少侠果然消息灵通。凝聚天地精华，汇集五行之力.若是哪位有缘人能交给老夫#Y999个“灵兜兜”，#W便能召唤传说中的五行神兽。#80'
                ],
            'options':
            [
                '兑换特殊魔兽要诀（消耗999神兜兜）','兑换超级鲲鹏（集齐999个灵兜兜右击获得）','我养不起'
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
