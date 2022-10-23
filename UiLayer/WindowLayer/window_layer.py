from Node.node import Node
import pygame
from Common.constants import *
from Node.image_rect import ImageRect
from Common.common import *


class Window(Node):
    """
    游戏窗口类
    """
    def __init__(self):
        super(Window, self).__init__()
        self.width, self.height = 400, 442
        self.window_title = '游戏窗口'

    def setup(self):
        # 背景裁切
        背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife4.rsp', 'hash_id': 0xC6476D82})
        背景.image = auto_sizing(背景.image, self.width, self.height, margin=1)
        背景.width, 背景.height = self.width, self.height
        self.add_child('背景', 背景)
        # 标题栏裁切, 居左
        标题栏 = set_node_attr(ImageRect(), {'rsp_file': 'wzife4.rsp', 'hash_id': 0x12989E68})
        标题栏.image = auto_sizing(标题栏.image, self.width - 35, 标题栏.height)
        标题栏.width, 标题栏.height = self.width, 标题栏.height
        标题栏.x += 4
        标题栏.y += 2
        self.add_child('标题栏', 标题栏)
        # 标题背景裁切, 居中
        标题背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife1.rsp', 'hash_id': 0x446087F2})
        self.add_child('标题背景', 标题背景)
        标题背景.image = auto_sizing(标题背景.image, 100, 标题背景.height)
        标题背景.width, 标题背景.height = 100, 标题背景.height
        标题背景.x = self.width//2 - 标题背景.width//2
        标题背景.y += 3
        # 标题居中
        from Node.label import Label
        标题 = Label(text=self.window_title, font_name=SIM_HEI, bold=True, size=15)
        标题.x = self.width//2 - 标题.width//2
        标题.y += 2
        self.add_child('标题', 标题)

        self.x = self.director.window_w//2 - self.width//2
        self.y = self.director.window_h//2 - self.height//2


class WindowLayer(Node):
    def __init__(self):
        super(WindowLayer, self).__init__()
        self.window_list = []  # 所有游戏窗口
        self.hover_window = None

    def append(self, win):
        self.window_list.append(win)

    @property
    def window_list_r(self):
        """
        window_list反序
        :return:
        """
        _list = self.window_list.copy()
        _list.reverse()
        return _list

    @property
    def active_window(self):
        """
        最上层的窗口, 活跃窗口
        :return:
        """
        # 返回列表末尾窗口(显示时在最上方)
        if len(self.window_list) > 0 and self.window_list[-1].visible:
            return self.window_list[-1]
        return None

    def window_switch(self, win, visible=None):
        """
        切换窗口可视状态
        :param win: 窗口类
        :param visible: 可视状态, True/False
        :return:
        """
        win.switch(visible)

        # 若窗口变为可视则加入队列, 且提升到最高层级
        if win.is_visible:
            if win in self.window_list:
                self.window_list.remove(win)
            self.append(win)

    def update(self):
        m_pos = pygame.mouse.get_pos()
        if self.director.match_mouse_event(self.mouse_filter, MOUSE_LEFT_RELEASE):
            if self.active_window is not None:
                self.active_window.is_pressed = False
        for win in self.window_list_r:
            if win == self.active_window:
                win.process_event()
            if win.is_visible and win.rect.collidepoint(m_pos):
                self.hover_window = win
                self.director.HERO_MOVE_FLAG = False  # 屏蔽主角行走
                # 右键关闭窗口
                if self.director.match_mouse_event(self.mouse_filter, MOUSE_RIGHT_RELEASE) and self.director.GRABBED_ITEM is None:
                    self.window_switch(win, False)
                    _ = self.director.mouse_event  # 清空鼠标事件, 避免右键关闭多个窗口

            # 非活跃窗口一律重置pressed状态
            if win != self.active_window:
                win.is_pressed = False
            # 非活跃窗口点击则置活跃状态
            if win.is_visible and win != self.active_window and win.rect.collidepoint(m_pos):
                if self.active_window is not None and self.active_window.rect.collidepoint(m_pos):
                    pass
                else:
                    if self.director.mouse_event == MOUSE_LEFT_DOWN:
                        self.window_switch(win, True)

        # 按照优先级显示窗口
        for win in self.window_list:
            if win.is_visible:
                win.update()

        if self.active_window is not None:
            # 活跃窗口被点击时置pressed状态
            if self.active_window.rect.collidepoint(m_pos) and self.director.mouse_event == MOUSE_LEFT_DOWN:
                self.active_window.is_pressed = True
                self.active_window.px, self.active_window.py = m_pos[0] - self.active_window.sx, m_pos[1] - self.active_window.sy
            # 活跃窗口鼠标拖动
            if self.active_window.is_pressed and self.director.IS_MOUSE_LEFT_PRESSED and self.active_window.window_name != '对话栏':
                self.active_window.sx, self.active_window.sy = m_pos[0] - self.active_window.px, m_pos[1] - self.active_window.py
