import os.path

from Node.node import Node
import pygame
from Common.constants import *
from Node.image_rect import ImageRect
from Common.common import *
from Node.button import ButtonClassicClose, Button
from Node.text_edit import TextEdit
from Common.socket_id import *


class Window(Node):
    """
    游戏窗口类
    """
    def __init__(self):
        super(Window, self).__init__()
        self.width, self.height = 400, 442
        self.window_title = '游戏窗口'
        self.is_pressed = False  # 鼠标按住
        self.press_x, self.press_y = 0, 0
        self.x = self.director.window_w // 2 - self.width // 2
        self.y = self.director.window_h // 2 - self.height // 2
        self.last_x, self.last_y = self.x, self.y  # 拖拽时使用, 上一次的xy坐标
        self.config_file = ''
        self.is_draggable = True

    @property
    def window_name(self):
        """
        窗口名称, 和节点名称相同
        :return:
        """
        return self.node_name

    @property
    def win_manager(self):
        return self.get_parent()

    @property
    def is_active(self):
        return self.win_manager.active_window == self.window_name

    def switch(self, visible):
        """
        切换可视状态
        :param visible:
        :return:
        """
        print('switch:', self.window_name, visible)
        self.visible = visible

    def setup_win_config(self, file=None, given_node=None):
        """
        从窗口配置文件加载窗口UI(添加子节点)
        :param file: 可以指定file,默认为self.config_file
        :param given_node: 可以给特定的子节点添加子节点, 比如窗口的特定区域
        :return:
        """
        if not given_node:
            given_node = self
        if not file:
            file = self.config_file
        if not file:
            return
        if not os.path.exists(file):
            print('窗口配置文件不存在:', file)
            return
        nodes = read_csv(file)
        for node_info in nodes:
            tp = node_info['\ufefftype']
            name = node_info['name']
            node = new_node(tp)
            node.x, node.y = int(node_info['x']), int(node_info['y'])
            w, h = node_info['width'], node_info['height']
            if w != '':
                node.width = int(w)
            if h != '':
                node.height = int(h)
            other_attrs = node_info['other'].split(';')
            for attr in other_attrs:
                if not attr:
                    continue
                attr_name, attr_value = attr.split(':')
                if attr_value.isdigit():
                    attr_value = int(attr_value)
                if attr_value == 'True':
                    attr_value = True
                if attr_value == 'False':
                    attr_value = False
                setattr(node, attr_name, attr_value)
            node.setup()
            given_node.add_child(name, node)

    def setup(self):
        # 背景裁切
        背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife4.rsp', 'hash_id': 0xC6476D82})
        背景.image = auto_sizing(背景.image, self.width, self.height, margin=1)
        背景.width, 背景.height = self.width, self.height
        self.add_child('背景', 背景)
        # 标题栏裁切, 居左
        标题栏 = set_node_attr(ImageRect(), {'rsp_file': 'wzife4.rsp', 'hash_id': 0x12989E68})
        标题栏.image = auto_sizing(标题栏.image, self.width - 29, 标题栏.height)
        标题栏.width, 标题栏.height = self.width, 标题栏.height
        标题栏.x += 4
        标题栏.y += 2
        self.add_child('标题栏', 标题栏)
        # 标题背景裁切, 标题文字, 居中
        标题背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife1.rsp', 'hash_id': 0x446087F2})
        self.add_child('标题背景', Node())  # 先占位, 后添加实际的标题背景节点

        from Node.label import Label
        标题 = Label(text=self.window_title, outline=True)
        标题.x = self.width // 2 - 标题.width // 2
        标题.y += 2
        self.add_child('标题', 标题)

        width = max(80, 标题.width + 20)
        标题背景.auto_sizing(w=width)
        标题背景.x = self.width // 2 - 标题背景.width // 2
        标题背景.y += 3
        self.add_child('标题背景', 标题背景)
        # 关闭按钮, 居右
        关闭按钮 = ButtonClassicClose()
        关闭按钮.x = self.width - 25
        关闭按钮.y += 4
        self.add_child('关闭按钮', 关闭按钮)

    def check_event(self):
        # super(Window, self).check_event()
        # 左键点击激活
        if self.is_hover:
            if self.is_active:
                if self.director.match_mouse_event(STOP, MOUSE_LEFT_DOWN):
                    self.win_manager.set_active_window(self.window_name)
                    self.is_pressed = True
                    self.press_x, self.press_y = pygame.mouse.get_pos()
        # 判断是否按住
        if self.is_hover:
            if self.director.match_mouse_event(STOP, MOUSE_LEFT_DOWN):
                self.is_pressed = True
                self.press_x, self.press_y = pygame.mouse.get_pos()
            elif self.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                self.is_pressed = False
                self.last_x, self.last_y = self.x, self.y
        else:  # 鼠标不在rect内则重置按下状态
            self.is_pressed = False
            self.last_x, self.last_y = self.x, self.y
        if self.director.is_mouse_left_released:  # 双重保障, 全局鼠标左键弹起标志位为true则说明鼠标没有按下
            self.is_pressed = False
            self.last_x, self.last_y = self.x, self.y
        # 按住拖动
        if self.is_pressed:
            mpos = pygame.mouse.get_pos()
            dx = self.press_x - mpos[0]
            dy = self.press_y - mpos[1]
            self.x = self.last_x - dx
            self.y = self.last_y - dy
        # 右键点击关闭
        if self.is_hover:
            if self.director.match_mouse_event(STOP, MOUSE_RIGHT_RELEASE):
                self.visible = False

        for child in self.get_children().values():
            # 点击子节点也激活自身
            if hasattr(child, 'is_pressed') and child.is_pressed:
                self.director.match_mouse_event(STOP, MOUSE_LEFT_DOWN)
                self.win_manager.set_active_window(self.window_name)

            # 如果自身非激活, 则所有输入框也取消激活
            if not self.is_active and type(child) == TextEdit:
                child.is_active = False


class WindowLayer(Node):
    """
    游戏的窗口管理器
    """
    def __init__(self):
        super(WindowLayer, self).__init__()
        self.window_list = []  # 所有游戏窗口
        self.hover_window = None

    @property
    def active_window(self):
        """
        最上层的窗口名称, 活跃窗口
        :return:
        """
        # 返回列表末尾窗口(显示时在最上方)
        if self.get_children_count() > 0:
            return list(self.get_children().keys())[-1]
        return None

    def set_active_window(self, name: str):
        if name == self.active_window:
            return
        print('set active:', name)
        for win_name, win in self.get_children().copy().items():
            if name == win_name:
                tmp_name, tmp_win = win_name, win
                self.remove_child(win_name)
                self.add_child(tmp_name, tmp_win)
                return

    def switch_window(self, win, visible=None):
        """
        切换窗口可视状态
        :param win: 窗口类 or 窗口名称
        :param visible: 可视状态, True/False
        :return:
        """
        if type(win) == str:
            win = self.child(win)
        # visible为None时切换可视状态, 指定visible可以指定可视状态
        if visible is None:
            visible = not win.visible
        win.switch(visible)

        # 若窗口变为可视则加入队列, 且提升到最高层级
        if win.visible:
            self.set_active_window(win)

    def check_event(self):
        super(WindowLayer, self).check_event()

        # alt W
        if self.director.alt_down and self.director.match_kb_event(STOP, pygame.K_w):
            self.switch_window(self.child('人物属性'))
        # alt Q
        if self.director.alt_down and self.director.match_kb_event(STOP, pygame.K_q):
            self.director.client.send(C_登陆, {'账号': 'admin1', '密码': 123456, '登陆id': 1001})
