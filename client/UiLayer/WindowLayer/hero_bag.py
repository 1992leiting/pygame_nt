import random

from UiLayer.WindowLayer.window_layer import Window
from UiLayer.WindowLayer.win_config import WinHeroAttr
from Common.constants import *
from Node.button import ToggleButtonGroup
from Node.object_block import ItemBlock, BlockGroup


class HeroBag(Window):
    def __init__(self):
        super(HeroBag, self).__init__()
        self.enable = False
        self.window_title = '道具行囊'
        self.width, self.height = 312, 452
        self.has_title_ui = True
        self.config_file = winconfig_dir + 'HeroBag.csv'
        self.info_page = 0  # 人物/召唤兽/坐骑/子女
        self.bag_page = 0  # 背包/行囊/任务/法宝
        self.setup()
        self.setup_win_config()

    def setup(self):
        super(HeroBag, self).setup()
        self.top_left_x = 0
        self.center_y = game.director.window_h//2

    def setup_item_blocks(self):
        # 物品格子
        block_group = BlockGroup()
        index = 0
        _x = 33 - 50
        for i in range(5):
            _x += 50.5
            _y = 200
            for j in range(4):
                block = ItemBlock()
                block_group.append(block)
                # block.setup(random.sample(['飞行符', '月饼', '烟花', '天眼通符', '藏宝图', '蟠桃', '光环碎片'], 1)[0])
                block.x, block.y = _x, _y
                block.index = index
                self.add_child('block' + str(index), block)
                index += 1
                _y += 51

    def setup_win_config(self, file=None, given_node=None):
        super(HeroBag, self).setup_win_config(file, given_node)
        btn_group = ToggleButtonGroup()
        self.add_child('page_btn_group', btn_group)  # 切换人物/召唤兽/坐骑/子女的按钮组
        btn_group = ToggleButtonGroup()
        self.add_child('bag_btn_group', btn_group)  # 切换背包/行囊的按钮组
        btn_group = ToggleButtonGroup()
        self.add_child('equip_btn_group', btn_group)  # 切换装备的按钮组
        self.child('page_btn_group').append(self.child('btn_人物'))
        self.child('page_btn_group').append(self.child('btn_召唤'))
        self.child('page_btn_group').append(self.child('btn_坐骑'))
        self.child('page_btn_group').append(self.child('btn_子女'))
        self.child('bag_btn_group').append(self.child('btn_背包'))
        self.child('bag_btn_group').append(self.child('btn_行囊'))
        self.child('bag_btn_group').append(self.child('btn_任务'))
        self.child('bag_btn_group').append(self.child('btn_法宝'))
        self.child('equip_btn_group').append(self.child('btn_1'))
        self.child('equip_btn_group').append(self.child('btn_2'))
        self.child('equip_btn_group').append(self.child('btn_3'))

        self.setup_item_blocks()

    def switch(self, visible):
        super(HeroBag, self).switch(visible)
        if visible:
            self.setup_win_config()

    def update(self):
        super(HeroBag, self).update()
        if self.child('btn_人物').is_toggled:
            self.info_page = 0
        elif self.child('btn_召唤').is_toggled:
            self.info_page = 1
        elif self.child('btn_坐骑').is_toggled:
            self.info_page = 2
        elif self.child('btn_子女').is_toggled:
            self.info_page = 3

        self.child('人物信息').enable = (self.info_page == 0)
        self.child('召唤兽信息').enable = (self.info_page == 1)
        self.child('坐骑信息').enable = (self.info_page == 2)
        self.child('子女信息').enable = (self.info_page == 3)

    def check_event(self):
        super(HeroBag, self).check_event()
        # if self.child('btn_技能') and self.child('btn_技能').event:
        #     self.win_manager.switch_window('人物技能')
