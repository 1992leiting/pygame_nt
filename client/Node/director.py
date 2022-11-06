from Node.node import Node
import pygame
from Common.common import *
from Common.constants import *
from Game.event_handler import EventHandler
from Game.astar import Astar
import socket
from Node.prompt import GamePromptManager
from Network.my_socket import SocketClient
from Common.socket_id import *


pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)


class Director(Node):
    """
    导演类, 游戏UI的根节点, 控制整个游戏的UI运行/切换/控制等
    """
    def __init__(self):
        super(Director, self).__init__(director=True)
        self.game_fps = 60
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
        self.mouse_left_down_time = 0  # 鼠标左键按下的时长
        self.event_handler = EventHandler(self)
        self.char_hover = None
        self.node_hover = None  # 当前处于hover状态的节点, 只允许有一个
        self.astar = Astar(self)
        self.is_hero_in_portal = False
        self.char_data = None
        self.item_data = None
        self.item_warehouse_data = None
        self.pet_data = None
        self.pet_warehouse_data = None

        self.socket = socket.socket()
        self.connect_server()
        self.client = SocketClient(self.socket, self.director)
        self.client.start()

        self.setup_ui()

    @property
    def gp_manager(self):
        return self.child('gp_manager')

    @property
    def window_size(self):
        return pygame.math.Vector2((self.window_w, self.window_h))

    @window_size.setter
    def window_size(self, arg):
        self.window_w, self.window_h = arg
        self.screen = pygame.display.set_mode(self.window_size, 0, 32)

    def setup_ui(self):
        self.add_child('scene', Node(director=True))
        self.add_child('function_layer', Node(director=True))
        self.add_child('window_layer', Node(director=True))
        self.add_child('floating_layer', Node(director=True))
        self.add_child('mouse', new_node('Mouse'))

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
        获取鼠标坐标(坐标再每个游戏帧开始时获取), 模式为STOP时, 会清空坐标值(屏幕外的坐标)
        效果类似鼠标点击获取, 避免UI重叠式重复获取到鼠标坐标, 影响hover判断
        :param mode:
        :return:
        """
        _pos = self.mouse_pos
        if mode == STOP:
            self.mouse_pos = (-100, -100)
        return _pos

    def get_kb_text(self):
        _text = self.kb_text
        self.kb_text = ''
        return _text

    def connect_server(self):
        try:
            self.socket.connect((SERVER_IP, SERVER_PORT))
        except:
            from Common.common import show_error, exit_game
            show_error('连接服务器失败!', '网络错误')
            exit_game()
        else:
            print('连接游戏服务器成功!')
    
    def update(self):
        self.node_hover = None
        self.mouse_pos = pygame.mouse.get_pos()
        # 移动镜头, 远快近慢优化镜头视觉效果
        hero = self.get_node('scene/world_scene/hero')
        camera = self.director.get_node('scene/world_scene/camera')
        if hero and camera and hero.visible:
            cdx, cdy = 0, 0
            if hero.map_x - camera.center_x > 100:
                cdx = MOVING_SPEED * (hero.map_x - camera.center_x - 100) // 10
            elif hero.map_x - camera.center_x > 1:
                cdx = 1
            if camera.center_x - hero.map_x > 100:
                cdx = -MOVING_SPEED * (camera.center_x - hero.map_x - 100) // 10
            elif camera.center_x - hero.map_x > 1:
                cdx = -1
            if hero.map_y - camera.center_y > 100:
                cdy = MOVING_SPEED * (hero.map_y - camera.center_y - 100) // 10
            elif hero.map_y - camera.center_y > 1:
                cdy = 1
            if camera.center_y - hero.map_y > 100:
                cdy = -MOVING_SPEED * (camera.center_y - hero.map_y - 100) // 10
            elif camera.center_y - hero.map_y > 1:
                cdy = -1
            camera.move(cdx, cdy)


game_director = Director()
