from Node.node import Node
from Game.res_manager import fill_image_rect, fill_animation8d
from Node.image_rect import ImageRect
from Common.common import *
from Common.constants import *
from Node.label import Label
from Node.animation import Animation8D


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
        self.left_click_callback = None
        self.right_click_callback = None
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

    # def check_event(self):
    #     super(ObjectBlock, self).check_event()
    #     if self.is_hover:
    #         if not self.is_checked and game.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
    #             self.is_checked = True
    #             if self.block_group:
    #                 self.block_group.set_block_checked(self)


class ItemBlock(ObjectBlock):
    def __init__(self):
        super(ItemBlock, self).__init__()
        self.item_name = ''
        self.item_data = []
        self.is_grasped = False  # 是否被抓住
        self.icon_rsp = ''
        self.icon_hash = 0
        self._event = None
        self.index = -1  # 序号,用于定位物品

    def reset(self):
        node = ImageRect()  # 图标
        self.add_child('icon', node)
        self.item_name = ''
        self.item_data = []
        self.is_grasped = False  # 是否被抓住
        self.icon_rsp = ''
        self.icon_hash = 0
        self._event = None
        self.index = -1  # 序号,用于定位物品

    def setup(self, item_name, data):
        if item_name not in BH_ITEM_DATA:
            print('物品不存在:', item_name)
            return
        self.item_name = item_name
        self.item_data = data
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
        # 显示详情
        if self.item_name and self.is_hover:
            big_icon_hash = BH_ITEM_DATA[self.item_name]['大图标']
            text = BH_ITEM_DATA[self.item_name]['说明']
            game.rp.show(self.icon_rsp, big_icon_hash, self.item_name, text)

    def check_event(self):
        super(ItemBlock, self).check_event()
        if self.is_hover:
            if self.item_name and not self.is_checked and game.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                print('item选中:', self.index, self.item_name)
                self.is_checked = True
                if self.block_group:
                    self.block_group.set_block_checked(self)
            if not self.is_grasped and game.director.match_mouse_event(STOP, MOUSE_RIGHT_RELEASE):
                print('item右击', self.index, self.item_name)
            if self.item_name and not self.is_grasped and self.is_checked and game.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                self.is_grasped = True
                fill_image_rect(game.mouse.child('grasp'), self.icon_rsp, self.icon_hash)
                print('item抓住', self.index, self.item_name)
        if self.is_grasped and game.director.match_mouse_event(STOP, MOUSE_RIGHT_RELEASE):
            self.is_grasped = False
            game.mouse.clear_grasp_icon()

class SkillBlock(ObjectBlock):
    def __init__(self):
        super().__init__()
        self.width, self.height = 50, 50
        self.skill_name = ''
        self.icon_rsp = ''
        self.icon_hash = 0
        self.left_click_callback = None
        self.right_click_callback = None
        self._event = None
        node = fill_animation8d(Animation8D(), 'wzife4.rsp', 0x5DC9B461)  # 焦点框
        node.enable = False
        self.add_child('hover_box', node)
        node.center_x, node.center_y = self.center_x-2, self.center_y

    def reset(self):
        node = ImageRect()  # 图标
        self.add_child('icon', node)
        self.skill_name = ''
        self.icon_rsp = ''
        self.icon_hash = 0
        self.left_click_callback = None
        self.right_click_callback = None
        self._event = None

    def setup(self, name):
        self.skill_name = name
        # 图标
        self.icon_rsp = BH_SKILL_DATA[name]['文件']
        self.icon_hash = BH_SKILL_DATA[name]['大图标']
        fill_image_rect(self.child('icon'), self.icon_rsp, self.icon_hash)
        self.child('icon').center_x, self.child('icon').center_y = self.center_x - 1, self.center_y

    def update(self):
        super().update()
        # 显示详情
        if self.skill_name and self.is_hover:
            big_icon_hash = BH_SKILL_DATA[self.skill_name]['大图标']
            text = BH_SKILL_DATA[self.skill_name]['介绍']
            if BH_SKILL_DATA[self.skill_name]['条件']:
                text = text + '\n#G【条件】' + BH_SKILL_DATA[self.skill_name]['条件']
            if BH_SKILL_DATA[self.skill_name]['消耗']:
                text = text + '\n#Y【消耗】' + BH_SKILL_DATA[self.skill_name]['消耗']
            if BH_SKILL_DATA[self.skill_name]['冷却']:
                text = text + '\n#P【冷却】' + BH_SKILL_DATA[self.skill_name]['冷却']
            game.rp.show(self.icon_rsp, big_icon_hash, self.skill_name, text)

    def check_event(self):
        super().check_event()
        if self.is_hover:
            if game.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                if self.left_click_callback:
                    self.left_click_callback(self.skill_name)
                print('技能点击:', self.skill_name)
            if game.director.match_mouse_event(STOP, MOUSE_RIGHT_RELEASE):
                if self.right_click_callback:
                    self.right_click_callback(self.skill_name)
