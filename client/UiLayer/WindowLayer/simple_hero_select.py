from UiLayer.WindowLayer.window_layer import Window
from Node.text_edit import LineEditWithBg
from Node.button import ButtonClassicRed
from Node.label import Label
from Common.socket_id import *
from Node.character import Character
from Common.constants import *


pos = [(100, 160), (250, 160), (400, 160), (100, 350), (250, 350), (400, 350)]


class SimpleHeroSelect(Window):
    def __init__(self):
        super(SimpleHeroSelect, self).__init__()
        self.visible = False
        self.window_title = '简易角色选择'
        self.width, self.height = 600, 400
        self.hero_data = []  # 角色数据
        self.setup()
        self.setup_win_config()

    def setup_win_config(self, file=None, given_node=None):
        for i in range(6):
            btn = ButtonClassicRed('进入', 60)
            btn.is_active = False
            btn.center_x = pos[i][0]
            btn.center_y = pos[i][1] + 20
            self.add_child('进入' + str(i), btn)

        btn = ButtonClassicRed('创建角色', 100)
        btn.center_x, btn.center_y = 520, 350 + 20
        self.add_child('创建角色', btn)

    def load_hero_data(self, hero_data):
        print('load hero:', hero_data)
        self.hero_data = hero_data
        for i, data in enumerate(hero_data):
            ch = Character()
            ch.set_data(data)
            ch.x = pos[i][0]
            ch.y = pos[i][1] - 40
            self.add_child('hero' + str(i), ch)
            # 按钮激活
            self.child('进入' + str(i)).is_active = True

    def check_event(self):
        super(SimpleHeroSelect, self).check_event()
        if self.child('创建角色').event:
            win = self.director.get_node('window_layer/简易创建角色')
            win.switch(True)

        for i in range(6):
            if self.child('进入' + str(i)).event:
                self.director.client.send(C_角色进入, dict(账号=game.account, pid=self.hero_data[i]['id']))
