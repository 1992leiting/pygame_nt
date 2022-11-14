from UiLayer.WindowLayer.window_layer import Window
from UiLayer.WindowLayer.win_config import WinHeroAttr
from Common.constants import *


class HeroAttr(Window):
    def __init__(self):
        super(HeroAttr, self).__init__()
        self.visible = False
        self.window_title = '人物状态'
        self.width, self.height = 258, 454
        self.x = self.director.window_w - self.width
        self.config_file = winconfig_dir + 'HeroAttr.csv'
        self.setup()
        self.setup_win_config()
        self.top_right_x = game.director.window_w - 1

    def check_event(self):
        super(HeroAttr, self).check_event()
        if self.child('btn_技能') and self.child('btn_技能').event:
            self.win_manager.switch_window('人物技能')
