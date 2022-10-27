from UiLayer.WindowLayer.window_layer import Window
from UiLayer.WindowLayer.win_config import WinHeroAttr
from Common.constants import *


class HeroAttr(Window):
    def __init__(self):
        super(HeroAttr, self).__init__()
        self.window_title = '人物状态'
        self.width, self.height = 258, 454
        self.config_file = winconfig_dir + 'HeroAttr.csv'
        self.setup()
        self.setup_win_config()
