from UiLayer.WindowLayer.window_layer import Window
from Node.text_edit import LineEditWithBg
from Common.constants import *


class SimpleLogin(Window):
    def __init__(self):
        super(SimpleLogin, self).__init__()
        self.visible = False
        self.window_title = '简易登陆'
        self.width, self.height = 300, 300
        self.setup()
        self.setup_win_config()

    def setup_win_config(self, file=None, given_node=None):
        account_input = LineEditWithBg()
        account_input.x, account_input.y = 100, 100
        account_input.width = 150
        account_input.setup()
        self.add_child('账号输入', account_input)

    # def check_event(self):
    #     super(SimpleLogin, self).check_event()
