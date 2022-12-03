from Node.node import Node
from Game.res_manager import fill_image_rect
from Node.image_rect import ImageRect
from Common.common import *
from Common.constants import *
from Node.label import Label


class BlockGroup(Node):
    def __init__(self):
        super(BlockGroup, self).__init__()
        self.blocks = []

    def append(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
            block.block_group = self

    def set_block_checked(self, block):
        """
        组中一个block选中其他的取消选中
        """
        for blk in self.blocks:
            if blk != block:
                blk.is_checked = False


class ObjectBlock(Node):
    def __init__(self):
        super(ObjectBlock, self).__init__()
        self.width, self.height = 50, 50
        self.is_checked = False  # 是否选中
        self.is_enabled = True  # 是否禁止
        self.is_stacked = False  # 是否可叠加
        node = ImageRect()  # 图标
        self.block_group = None  # 所属的block group
        self.add_child('icon', node)
        node = Label(text=1, outline=True)  # 数字
        node.x, node.y = 4, 4
        node.enable = False
        self.add_child('number', node)
        node = fill_image_rect(ImageRect(), 'wzife.rsp', 0x6F88F494)  # 焦点框
        node.enable = False
        self.add_child('hover_box', node)
        node.center_x, node.center_y = self.center_x, self.center_y
        node = fill_image_rect(ImageRect(), 'wzife.rsp', 0x10921CA7)  # 选中框
        node.enable = False
        self.add_child('check_box', node)
        node.center_x, node.center_y = self.center_x, self.center_y
        node = fill_image_rect(ImageRect(), 'wzife.rsp', 0x4138B067)  # 禁止框
        node.enable = False
        self.add_child('disable_box', node)
        node.center_x, node.center_y = self.center_x, self.center_y

    def update(self):
        super(ObjectBlock, self).update()
        self.child('hover_box').enable = self.is_hover
        self.child('check_box').enable = self.is_checked
        self.child('disable_box').enable = not self.is_enabled
        self.child('number').enable = self.is_stacked

    def check_event(self):
        super(ObjectBlock, self).check_event()
        if self.is_hover:
            if not self.is_checked and game.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                self.is_checked = True
                if self.block_group:
                    self.block_group.set_block_checked(self)


class ItemBlock(ObjectBlock):
    def __init__(self):
        super(ItemBlock, self).__init__()
        self.item_name = ''
        self.item_data = []
        self.is_grasped = False  # 是否被抓住
        self.icon_rsp = ''
        self.icon_hash = 0
        self.callback_func = None
        self._event = None

    def setup(self, item_name):
        if item_name not in BH_ITEM_DATA:
            print('物品不存在:', item_name)
            return
        self.item_name = item_name
        # 图标
        self.icon_rsp = BH_ITEM_DATA[item_name]['文件']
        self.icon_hash = BH_ITEM_DATA[item_name]['小图标']
        fill_image_rect(self.child('icon'), self.icon_rsp, self.icon_hash)
        self.child('icon').center_x, self.child('icon').center_y = 23, 25
        # 叠加
        self.is_stacked = BH_ITEM_DATA[item_name]['叠加']

    def update(self):
        super(ItemBlock, self).update()
        self.child('number').enable = (not self.is_grasped) and self.is_stacked
        self.child('icon').enable = not self.is_grasped

    def check_event(self):
        super(ItemBlock, self).check_event()
        if self.is_hover:
            if not self.is_grasped and game.director.match_mouse_event(STOP, MOUSE_RIGHT_RELEASE):
                print('item右击', self.item_name)
            if not self.is_grasped and self.is_checked and game.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                self.is_grasped = True
                fill_image_rect(game.mouse.child('grasp'), self.icon_rsp, self.icon_hash)
                print('item抓住', self.item_name)
        if self.is_grasped and game.director.match_mouse_event(STOP, MOUSE_RIGHT_RELEASE):
            self.is_grasped = False
            game.mouse.clear_grasp_icon()
        if self.callback_func:
            self.callback_func(self._event)
