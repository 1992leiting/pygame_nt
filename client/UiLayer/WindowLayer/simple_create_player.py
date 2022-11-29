from UiLayer.WindowLayer.window_layer import Window
from Node.text_edit import LineEditWithBg
from Node.button import ButtonClassicRed
from Node.label import Label
from Common.socket_id import *
from Common.common import *


class SimpleCreatePlayer(Window):
    def __init__(self):
        super(SimpleCreatePlayer, self).__init__()
        self.enable = False
        self.window_title = '简易创建角色'
        self.width, self.height = 300, 300
        self.setup()
        self.setup_win_config()

    def setup_win_config(self, file=None, given_node=None):
        _text = Label(text='角色')
        _text.x, _text.y = 50, 100
        self.add_child('txt_角色', _text)
        _text = Label(text='名称')
        _text.x, _text.y = 50, 150
        self.add_child('txt_名称', _text)

        _input = LineEditWithBg()
        _input.line_edit.is_readonly = False
        _input.x, _input.y = 100, 100
        _input.width = 150
        _input.text = '龙太子'
        _input.setup()
        self.add_child('角色输入', _input)
        _input = LineEditWithBg()
        _input.line_edit.is_readonly = False
        _input.x, _input.y = 100, 150
        _input.width = 150
        _input.text = ''
        _input.setup()
        self.add_child('名称输入', _input)

        _btn = ButtonClassicRed('创建', 60)
        _btn.x, _btn.y = 190, 200
        self.add_child('创建', _btn)
        _btn = ButtonClassicRed('退出', 60)
        _btn.x, _btn.y = 100, 200
        self.add_child('退出', _btn)

    def check_event(self):
        super(SimpleCreatePlayer, self).check_event()
        from Common.constants import game
        if self.child('创建').event:
            account = game.account
            model = self.child('角色输入').text
            name = self.child('名称输入').text
            self.director.client.send(C_创建角色, dict(账号=account, 模型=model, 名称=name))

