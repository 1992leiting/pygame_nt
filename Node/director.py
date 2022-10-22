from Node.node import Node
import pygame
from Common.constants import *
from Game.event_handler import EventHandler
from Game.astar import Astar


pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)


class Director(Node):
    """
    导演类, 游戏UI的根节点, 控制整个游戏的UI运行/切换/控制等
    """
    def __init__(self):
        super(Director, self).__init__()
        self.game_fps = 30
        self.window_w = 800
        self.window_h = 600
        self.screen = pygame.display.set_mode(self.window_size, 0, 32)
        self.is_in_battle = False  # 是否在战斗中
        self.mouse_event = None  # 记录每个刷新回合的鼠标事件
        self.kb_event = None  # 记录每个刷新回合的键盘事件, [案件类型up/down, 键位]
        self.kb_text = ''  # 记录每个刷新回合的键盘文本输入
        self.alt_down = False  # 判断组合键
        self.ctrl_down = False  # 判断组合键
        self.key_down = None  # 键盘按键
        self.text_input = None
        self.is_mouse_left_released, self.is_mouse_right_released = False, False  # 鼠标左/右键是否处于按下状态
        self.te_manager = None  # 输入框管理器
        self.te_hover = None  # 鼠标指向的输入框
        self.mouse_scroll_y = 0  # 鼠标滚轮滚动的数量
        self.mouse_pos = None  # 鼠标坐标的暂存变量
        self.mouse_left_down_time = 9999999999  # 鼠标左键按下的时长
        self.event_handler = EventHandler(self)
        self.char_hover = None
        self.astar = Astar(self)
        self.is_hero_in_portal = False

    @property
    def window_size(self):
        return pygame.math.Vector2((self.window_w, self.window_h))

    @window_size.setter
    def window_size(self, arg):
        self.window_w, self.window_h = arg
        self.screen = pygame.display.set_mode(self.window_size, 0, 32)

    def match_mouse_event(self, mode, event):
        """
        匹配鼠标事件, 模式为STOP时, 只有匹配结果为True才清空事件
        :param mode:
        :param event:
        :return:
        """
        if mode == IGNORE:
            return None
        elif mode == PASS:
            return self.mouse_event == event
        else:
            _event = self.mouse_event
            if _event == event:
                self.mouse_event = None
                return True
            else:
                return False

    def get_mouse_scroll(self, mode):
        _scroll = self.mouse_scroll_y
        if mode == STOP:
            self.mouse_scroll_y = 0
        return _scroll

    def match_kb_event(self, mode, event):
        """
        匹配键盘事件, 模式为STOP时, 只有匹配结果为True才清空事件
        :param mode:
        :param event:
        :return:
        """
        if mode == IGNORE:
            return None
        elif mode == PASS:
            return self.kb_event == event
        else:
            _event = self.kb_event
            if _event == event:
                self.kb_event = None
                return True
            else:
                return False

    def get_mouse_pos(self, mode):
        """
        获取鼠标坐标(坐标再每个游戏帧开始时获取), 模式为STOP时, 会清空坐标值
        效果类似鼠标点击获取, 避免UI重叠式重复获取到鼠标坐标, 影响hover判断
        :param mode:
        :return:
        """
        _pos = self.mouse_pos
        if mode == STOP:
            self.mouse_pos = None
        return _pos

    def get_kb_text(self):
        _text = self.mouse_event
        self.kb_text = ''
        return _text
