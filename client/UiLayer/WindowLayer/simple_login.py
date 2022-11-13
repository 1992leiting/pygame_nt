from UiLayer.WindowLayer.window_layer import Window
from Node.text_edit import LineEditWithBg
from Node.button import ButtonClassicRed
from Node.label import Label
from Common.socket_id import *


class SimpleLogin(Window):
    def __init__(self):
        super(SimpleLogin, self).__init__()
        self.visible = False
        self.window_title = '简易登陆'
        self.width, self.height = 300, 300
        self.setup()
        self.setup_win_config()

    def setup_win_config(self, file=None, given_node=None):
        _text = Label(text='账号')
        _text.x, _text.y = 50, 100
        self.add_child('txt_账号', _text)
        _text = Label(text='密码')
        _text.x, _text.y = 50, 150
        self.add_child('txt_密码', _text)

        _input = LineEditWithBg()
        _input.line_edit.is_readonly = False
        _input.x, _input.y = 100, 100
        _input.width = 150
        _input.text = 'admin1'
        _input.setup()
        self.add_child('账号输入', _input)
        _input = LineEditWithBg()
        _input.line_edit.is_readonly = False
        _input.x, _input.y = 100, 150
        _input.width = 150
        _input.text = '123456'
        _input.setup()
        self.add_child('密码输入', _input)

        _btn = ButtonClassicRed('登陆', 60)
        _btn.x, _btn.y = 190, 200
        self.add_child('登陆', _btn)
        _btn = ButtonClassicRed('注册', 60)
        _btn.x, _btn.y = 100, 200
        self.add_child('注册', _btn)

    def check_event(self):
        super(SimpleLogin, self).check_event()
        if self.child('登陆').event:
            acc = self.child('账号输入').text
            pwd = self.child('密码输入').text
            print('登陆请求:', acc, pwd)
            self.director.client.send(C_账号登陆, dict(账号=acc, 密码=pwd))
        if self.child('注册').event:
            win_register = self.director.get_node('window_layer/简易注册')
            win_register.switch(True)
