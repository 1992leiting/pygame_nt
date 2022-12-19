from Node.node import Node
from Common.common import *
from Common.constants import *
from Common.socket_id import *
from Node.button import Button
from Node.image_rect import ImageRect

dy = 20

class BattleCmdMenu(Node):
    def __init__(self):
        super().__init__()
        self.add_child('char_cmd', Node())
        self.child('char_cmd').x = game.director.window_w - 150
        self.child('char_cmd').y = 150
        self.add_child('pet_cmd', Node())
        self.child('pet_cmd').x = game.director.window_w - 150
        self.child('pet_cmd').y = 150

        self.child('char_cmd').add_child('bg', set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xF5A9A3F5, 'x': -3, 'y': dy*0-2}))
        self.child('char_cmd').child('bg').auto_sizing(h=248)
        self.child('char_cmd').add_child('法术', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x839C6C7D, 'y': dy*0}))
        self.child('char_cmd').add_child('法宝', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x2E8F2187, 'y': dy*1}))
        self.child('char_cmd').add_child('特技', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x389DCCF5, 'y': dy*2}))
        self.child('char_cmd').add_child('道具', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x1587C26E, 'y': dy*3}))
        self.child('char_cmd').add_child('防御', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xA662D44B, 'y': dy*4}))
        self.child('char_cmd').add_child('保护', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x0467A0A8, 'y': dy*5}))
        self.child('char_cmd').add_child('指挥', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x8A8A21AD, 'y': dy*6}))
        self.child('char_cmd').add_child('召唤', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xA2E2DC42, 'y': dy*7}))
        self.child('char_cmd').add_child('召还', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xE1A79F93, 'y': dy*8}))
        self.child('char_cmd').add_child('自动', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xEFB4F757, 'y': dy*9}))
        self.child('char_cmd').add_child('捕捉', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x2ACB414D, 'y': dy*10}))
        self.child('char_cmd').add_child('逃跑', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x132041E1, 'y': dy*11}))

        self.child('pet_cmd').add_child('bg', set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xB5B958DF, 'x': -3, 'y': dy*0-2}))
        self.child('pet_cmd').child('bg').auto_sizing(h=108)
        self.child('pet_cmd').add_child('法术', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x839C6C7D,'y': dy*0}))
        self.child('pet_cmd').add_child('道具', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x1587C26E,'y': dy*1}))
        self.child('pet_cmd').add_child('防御', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xA662D44B,'y': dy*2}))
        self.child('pet_cmd').add_child('保护', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x0467A0A8,'y': dy*3}))
        self.child('pet_cmd').add_child('逃跑', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x132041E1,'y': dy*4}))

    @property
    def char_cmd(self):
        return self.child('char_cmd')

    @property
    def pet_cmd(self):
        return self.child('pet_cmd')

    def update(self):
        super().update()
        if game.battle_scene.status == ST_人物命令:
            self.char_cmd.visible = True
            self.pet_cmd.visible = False
        elif game.battle_scene.status == ST_召唤兽命令:
            self.char_cmd.visible = False
            self.pet_cmd.visible = True
        else:
            self.char_cmd.visible = False
            self.pet_cmd.visible = False

    def check_event(self):
        if self.child('char_cmd').child('法术').event:
            game.window_layer.switch_window('战斗技能栏')
