from Node.node import Node
from Common.common import *
from Common.constants import *
from Common.socket_id import *
from Node.button import Button

dy = 20

class BattleCmdMenu(Node):
    def __init__(self):
        super().__init__()
        self.add_child('char_cmd', Node())
        self.child('char_cmd').x = game.director.window_w - 150
        self.child('char_cmd').y = 150
        self.child('char_cmd').add_child('111', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xF5A9A3F5, 'y': dy*0}))
        self.child('char_cmd').add_child('111', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x839C6C7D, 'y': dy*0}))
        self.child('char_cmd').add_child('112', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x2E8F2187, 'y': dy*1}))
        self.child('char_cmd').add_child('113', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x389DCCF5, 'y': dy*2}))
        self.child('char_cmd').add_child('114', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x1587C26E, 'y': dy*3}))
        self.child('char_cmd').add_child('115', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xA662D44B, 'y': dy*4}))
        self.child('char_cmd').add_child('116', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x0467A0A8, 'y': dy*5}))
        self.child('char_cmd').add_child('117', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x8A8A21AD, 'y': dy*6}))
        self.child('char_cmd').add_child('118', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xA2E2DC42, 'y': dy*7}))
        self.child('char_cmd').add_child('119', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xE1A79F93, 'y': dy*8}))
        self.child('char_cmd').add_child('120', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0xEFB4F757, 'y': dy*9}))
        self.child('char_cmd').add_child('121', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x2ACB414D, 'y': dy*10}))
        self.child('char_cmd').add_child('122', set_node_attr(Button(), {'rsp_file': 'wzife.rsp', 'hash_id': 0x132041E1, 'y': dy*11}))
