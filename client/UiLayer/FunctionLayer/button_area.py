import random

from Node.button import Button
from Node.image_rect import ImageRect
from Node.node import Node
from Common.constants import *
import pygame
from Common.socket_id import *


class ButtonArea(Node):
    def __init__(self):
        super(ButtonArea, self).__init__()

        from Common.common import set_node_attr
        self.底图 = set_node_attr(ImageRect(), {'rsp_file': 'wzife2.rsp',
                                              'hash_id': 0x3D1FA249,
                                              'bottom_right_x': self.director.window_w,
                                              'bottom_right_y': self.director.window_h})
        self.add_child('底图', self.底图)
        self.btn_攻击 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 0x6BBC42FA,
                                               'x': self.director.window_w - 346,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_攻击', self.btn_攻击)
        self.btn_物品 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 240383749,
                                               'x': self.director.window_w - 320,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_物品', self.btn_物品)
        self.btn_给予 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 2119033822,
                                               'x': self.director.window_w - 294,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_给予', self.btn_给予)
        self.btn_交易 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 3400579252,
                                               'x': self.director.window_w - 269,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_交易', self.btn_交易)
        self.btn_队伍 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 222208523,
                                               'x': self.director.window_w - 243,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_队伍', self.btn_队伍)
        self.btn_宠物 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 410697672,
                                               'x': self.director.window_w - 218,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_宠物', self.btn_宠物)
        self.btn_任务 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 2706543282,
                                               'x': self.director.window_w - 191,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_任务', self.btn_任务)
        self.btn_帮派 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 3277532867,
                                               'x': self.director.window_w - 164,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_帮派', self.btn_帮派)
        self.btn_快捷 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 3144573054,
                                               'x': self.director.window_w - 137,
                                               'y': self.director.window_h - 35})
        self.add_child('btn_快捷', self.btn_快捷)
        self.btn_好友 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 2088395993,
                                               'x': self.director.window_w - 110,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_好友', self.btn_好友)
        self.btn_成就 = set_node_attr(Button(), {'rsp_file': 'wzife2.rsp',
                                               'hash_id': 2335878618,
                                               'x': self.director.window_w - 81,
                                               'y': self.director.window_h - 31})
        self.add_child('btn_成就', self.btn_成就)
        self.btn_动作 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 1417762464,
                                               'x': self.director.window_w - 53,
                                               'y': self.director.window_h - 37})
        self.add_child('btn_动作', self.btn_动作)
        self.btn_系统 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                               'hash_id': 1360459743,
                                               'x': self.director.window_w - 26,
                                               'y': self.director.window_h - 36})
        self.add_child('btn_系统', self.btn_系统)

    def check_event(self):
        if self.child('btn_攻击').event or (self.director.alt_down and self.director.match_kb_event(STOP, pygame.K_a)):
            self.director.gp_manager.append('此功能尚未实现, 敬请期待#' + str(random.randrange(10, 20)))
        if self.child('btn_物品').event or (self.director.alt_down and self.director.match_kb_event(STOP, pygame.K_e)):
            # self.director.client.send(C_创建账号, dict(账号='admin1', 密码=123456))
            # self.director.client.send(C_创建角色, dict(账号='admin1', 名称='我要变强2', 模型='龙太子'))
            self.director.client.send(C_登陆, dict(账号='admin1', 密码='123456', pid='10001'))

