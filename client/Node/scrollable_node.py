from Node.node import Node
from Common.common import *
from Common.constants import *
from Node.scrollbar import Scrollbar


class ScrollableNode(Node):
    def __init__(self):
        super().__init__()
        self._max_height = 1  # 最大高度
        self._scroll_value = 0  # 当前滚动的数值(像素数)
        self.disp_height = 1  # 显示的高度
        self.scroll_step = 1  # 滚动步进, 像素点数

    def bind_scroll_bar(self, bar:Scrollbar):
        """
        绑定滚动条
        """
        bar.binding_node = self
        bar.height = self.height
        self.add_child('scroll_bar', bar)
        self.scroll_bar.ori_x = self.width
        # self.scroll_bar.update_bar_height()

    @property
    def scroll_bar(self) -> Scrollbar:
        return self.child('scroll_bar')

    @property
    def max_height(self):
        return self._max_height

    @max_height.setter
    def max_height(self, h):
        """
        max_height变化时,触发滚动条长度变化
        """
        self._max_height = h
        if self.scroll_bar:
            self.scroll_bar.update_bar_height()
            self.scroll_bar.sync_ratio_from_binding_node(self.ratio)

    @property
    def ratio(self):
        return -self.scroll_value/(self.max_height - self.disp_height)

    @ratio.setter
    def ratio(self, r):
        self.scroll_value = -r * (self.max_height - self.disp_height)

    @property
    def scroll_value(self):
        """
        当前滚动的数值(像素数)
        """
        return self._scroll_value

    @scroll_value.setter
    def scroll_value(self, p):
        """
        当前滚动的数值(像素数)
        """
        self._scroll_value = p
        self.scroll_to_pos()

    def scroll_up(self, step:int=0):
        """
        上翻, step为像素点数
        """
        if not step:
            step = self.scroll_step
        self.scroll_value += step
        if self.scroll_bar:
            self.scroll_bar.sync_ratio_from_binding_node(self.ratio)

    def scroll_down(self, step:int=0):
        """
        下翻, step为像素点数
        """
        if not step:
            step = self.scroll_step
        self.scroll_value -= step
        if self.scroll_bar:
            self.scroll_bar.sync_ratio_from_binding_node(self.ratio)

    def scroll(self, px):
        """
        滚动具体的长度(像素数)
        """
        print('scroll:', px)
        self._scroll_value += px
        if self.scroll_bar:
            self.scroll_bar.ratio = self.ratio

    def scroll_to_ratio(self, r):
        """
        滚动到指定的比例点
        """
        self.ratio = r

    def scroll_to_pos(self, pos=None):
        """
        滚动到指定的位置, 实际节点需要进行重写
        """
        if pos:
            self._scroll_value = pos

        # 限定scroll_value范围
        if self.max_height <= self.disp_height:
            self._scroll_value = 0
        else:
            self._scroll_value = clamp(self._scroll_value, -self.max_height + self.disp_height, 0)

    def scroll_to_top(self):
        self.ratio = 0

    def scroll_to_bottom(self):
        self.ratio = 1

    def check_event(self):
        if self.is_hover:
            s = self.director.get_mouse_scroll(self.mouse_filter) * self.scroll_step  # 鼠标滚动转换为滚动像素数量
            if s:
                self.scroll(s)
