from Node.node import Node
from Game.res_manager import fill_res, fill_button
from Node.button import Button
from Common.constants import *
from Common.common import *
import pygame


class BarButton(Button):
    def __init__(self):
        super().__init__()

    def check_event(self):
        # 判断按住
        if self.is_hover:
            if self.director.match_mouse_event(STOP, MOUSE_LEFT_DOWN):
                self.is_pressed = True
                self.last_x, self.last_y = self.x, self.y
                self.press_x, self.press_y = pygame.mouse.get_pos()  # 按下时记录鼠标y坐标
            if self.is_pressed and self.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                self.is_pressed = False
        if self.is_pressed and self.director.is_mouse_left_released:
            self.is_pressed = False
            self.last_x, self.last_y = self.x, self.y


class Scrollbar(Node):
    def __init__(self):
        super().__init__()
        self.width = 18
        self.height = 100
        self._ratio = 0
        self.binding_node = None  # 绑定节点(可滚动节点)

        btn = Button()
        fill_res(btn, 'wzife.rsp', 0xFD3D61F2)  # 上翻按钮,18*19
        self.add_child('scroll_up', btn)

        btn = Button()
        fill_res(btn, 'wzife.rsp', 0x09217E13)  # 下翻按钮,18*19
        self.add_child('scroll_down', btn)

        btn = BarButton()
        fill_button(btn, 'wzife4.rsp', 0x88E9B473)  # 滑动条
        self.add_child('scroll_bar', btn)

    @property
    def button_up(self) -> Button:
        return self.child('scroll_up')

    @property
    def button_down(self) -> Button:
        return self.child('scroll_down')

    @property
    def bar(self) -> BarButton:
        return self.child('scroll_bar')

    def update_ratio(self):
        """
        当前滚动条位置所代表的比例
        """
        # print('update ratio:', self.height, self.bar.height, self.bar.ori_y)
        scroll_range = self.height - self.button_up.height - self.button_down.height - self.bar.height
        bar_top_pos = self.bar.ori_y - self.button_up.height
        self.ratio = bar_top_pos/scroll_range

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, r):
        self._ratio = r
        self.update_bar_pos()

    def sync_ratio_from_binding_node(self, r):
        """
        同步绑定节点的ratio, 不会再反过来去更新绑定节点避免死循环设置
        """
        self._ratio = r
        self.update_bar_pos(False)

    def update_bar_pos(self, update_binding_node=True):
        """
        根据当前ratio更新滚动条位置
        update_binding_node: 是否更新绑定节点
        """
        scroll_range = self.height - self.button_up.height - self.button_down.height - self.bar.height
        bar_top_pos = int(scroll_range * self.ratio)
        self.bar.ori_y = bar_top_pos + self.button_up.height
        # print('ratio:', self.ratio)
        # 如果有绑定节点,更新绑定节点滚动值
        if self.binding_node and update_binding_node:
            self.binding_node.ratio = self.ratio

    def update_bar_height(self):
        max_height = self.binding_node.max_height
        disp_height = self.binding_node.disp_height
        scroll_range = self.height - self.button_up.height - self.button_down.height
        bar_height = scroll_range * (disp_height/max_height)
        self.bar.height = clamp(bar_height, 30, scroll_range)
        print('sb update bar height:', max_height, disp_height, self.height, scroll_range, self.bar.height)
        self.bar.auto_sizing()

    def setup(self):
        h_up = self.button_up.height  # 上翻按钮高度
        h_down = self.button_down.height  # 下翻按钮高度
        if self.height <= (h_up + h_down + 20):
            self.height = h_up + h_down + 20

        # 设置按钮和滚动条位置
        self.button_down.ori_y = self.height - self.button_down.height
        self.bar.ori_y = self.button_up.height

        self.update_bar_height()

    def check_event(self):
        super().check_event()
        # 上翻/下翻按钮触发绑定节点的上翻/下翻动作
        if self.button_up.event:
            if self.binding_node:
                self.binding_node.scroll_up()
        if self.button_down.event:
            if self.binding_node:
                self.binding_node.scroll_down()

    def draw(self):
        super().draw()
        pygame.draw.rect(game.director.screen, (255, 255, 0), (self.x, self.y + self.button_up.height - 2, self.bar.width, self.height - self.button_up.height - self.button_down.height + 4), 1)

    def update(self):
        if self.bar.is_pressed:
            mpos = pygame.mouse.get_pos()
            # dx = self.bar.press_x - mpos[0]
            dy = self.bar.press_y - mpos[1]
            self.bar.y = self.bar.last_y - dy
            # 限制滚动条的坐标
            self.bar.ori_y = max(self.button_up.height, self.bar.ori_y)
            self.bar.ori_y = min(self.height - self.button_down.height - self.bar.height, self.bar.ori_y)
            self.update_ratio()

        # 同步绑定节点的ratio
        if self.binding_node:
            if self.ratio != self.binding_node.ratio:
                self.sync_ratio_from_binding_node(self.binding_node.ratio)
