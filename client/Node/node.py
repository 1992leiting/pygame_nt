import time
import pygame
from numpy import rec
from Common.constants import *
import pickle
from uuid import uuid4
from Common.constants import game


class Node:
    """
    基础节点类，其他所有UI类型都继承Node
    Node提供各种基础属性和方法
    """
    def __init__(self):
        self.node_name = ''
        self.level = 0  # 节点层级, 根节点为0级, 其子节点为1级, 类推
        self.uuid = str(uuid4())  # 唯一标识符
        self._visible = True
        self._parent = None
        self._enable = True
        self._children = {}
        self.ori_x, self.ori_y = 0, 0  # 原始坐标, 相对于父节点的坐标
        self.press_x, self.press_y = 0, 0  # 鼠标按下时坐标
        self.last_x, self.last_y = 0, 0  # 拖拽时使用, 上一次记录的xy
        self.shift_x, self.shift_y = 0, 0  # 显示时xy偏移
        self.is_draggable = False  # 是否运行拖动
        self.kx, self.ky = 0, 0
        self.width, self.height = 0, 0
        self._surface = None
        self.ysort = False  # 按y坐标进行排序
        self.mouse_filter = STOP
        self.timer = 0
        self.is_pressed = False  # 鼠标按下
        self.is_hover = False  # 是否hover
        self._hover_enabled = True  # 是否检测hover

    @property
    def director(self):
        return game.director

    @property
    def is_hover_enabled(self):
        return self._hover_enabled

    @is_hover_enabled.setter
    def is_hover_enabled(self, v):
        self._hover_enabled = v
        # 所有子类设置相同的值
        for child in self.get_children().copy().values():
            child.is_hover_enabled = v

    def check_hover(self):
        mpos = pygame.mouse.get_pos()
        if self.director.node_hover is None and self.rect.collidepoint(mpos):
            self.director.node_hover = self
            self.is_hover = True
        else:
            self.is_hover = False

    @property
    def surface(self):
        if not self._surface:
            return self.director.screen
        else:
            return self._surface

    @surface.setter
    def surface(self, sf):
        self._surface = sf

    @property
    def size(self):
        return self.width, self.height

    """
    x, y是节点的全局坐标(自身坐标所有父节点坐标的和), 位置为左上角
    也是节点在屏幕上的坐标
    """
    @property
    def x(self):
        if self._parent:
            return self.ori_x + self._parent.x
        else:
            return self.ori_x

    @property
    def y(self):
        if self._parent:
            return self.ori_y + self._parent.y
        else:
            return self.ori_y

    @x.setter
    def x(self, xx):
        if self._parent:
            self.ori_x = xx - self._parent.x
        else:
            self.ori_x = xx

    @y.setter
    def y(self, yy):
        if self._parent:
            self.ori_y = yy - self._parent.y
        else:
            self.ori_y = yy

    """
    在地图中的坐标, 可能需要根据继承关系改写
    character直接作为world子节点时, 则为self.ori_x/self.ori_y
    """

    @property
    def map_x(self):
        return self.ori_x

    @property
    def map_y(self):
        return self.ori_y

    @map_x.setter
    def map_x(self, xx):
        self.ori_x = xx

    @map_y.setter
    def map_y(self, yy):
        self.ori_y = yy

    """
    游戏坐标, 梦幻的坐标是真实坐标/20
    """

    @property
    def game_x(self):
        return self.ori_x // 20

    @game_x.setter
    def game_x(self, xx):
        self.ori_x = xx * 20

    @property
    def game_y(self):
        return self.ori_y // 20

    @game_y.setter
    def game_y(self, yy):
        self.ori_y = yy * 20

    @property
    def center_x(self):
        return self.x + self.width / 2

    @center_x.setter
    def center_x(self, xx):
        self.x = xx - self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    @center_y.setter
    def center_y(self, yy):
        self.y = yy - self.height / 2

    @property
    def top_left_x(self):
        return self.x

    @top_left_x.setter
    def top_left_x(self, xx):
        self.x = xx

    @property
    def top_left_y(self):
        return self.y

    @top_left_y.setter
    def top_left_y(self, yy):
        self.y = yy

    @property
    def top_right_x(self):
        return self.x + self.width

    @top_right_x.setter
    def top_right_x(self, xx):
        self.x = xx - self.width

    @property
    def top_right_y(self):
        return self.y

    @top_right_y.setter
    def top_right_y(self, yy):
        self.y = yy

    @property
    def mid_left_x(self):
        return self.x

    @mid_left_x.setter
    def mid_left_x(self, xx):
        self.x = xx

    @property
    def mid_left_y(self):
        return self.y + self.height / 2

    @mid_left_y.setter
    def mid_left_y(self, yy):
        self.y = yy - self.height / 2

    @property
    def mid_right_x(self):
        return self.x + self.width

    @mid_right_x.setter
    def mid_right_x(self, xx):
        self.x = xx - self.width

    @property
    def mid_right_y(self):
        return self.y + self.height / 2

    @mid_right_y.setter
    def mid_right_y(self, yy):
        self.y = yy - self.height / 2

    @property
    def bottom_left_x(self):
        return self.x

    @bottom_left_x.setter
    def bottom_left_x(self, xx):
        self.x = xx

    @property
    def bottom_left_y(self):
        return self.y + self.height

    @bottom_left_y.setter
    def bottom_left_y(self, yy):
        self.y = yy - self.height

    @property
    def bottom_right_x(self):
        return self.x + self.width

    @bottom_right_x.setter
    def bottom_right_x(self, xx):
        self.x = xx - self.width

    @property
    def bottom_right_y(self):
        return self.y + self.height

    @bottom_right_y.setter
    def bottom_right_y(self, yy):
        self.y = yy - self.height

    """
    父节点可视的情况下, 根据自身可视判断
    父节点不可视的情况下, 状态为不可视
    """
    @property
    def visible(self):
        if self._parent:
            return self._visible and self._parent.visible
        else:
            return self._visible

    @visible.setter
    def visible(self, v):
        self._visible = v

    @property
    def enable(self):
        if self._parent:
            return self._enable and self._parent.enable
        else:
            return self._enable

    @enable.setter
    def enable(self, v):
        self._enable = v

    """
    ysort时根据z值来排序
    默认情况下z=y, 特殊情况z需要重新计算
    """
    @property
    def z(self):
        return self.y

    @property
    def rect(self):
        # rect = pygame.Rect(self.x - self.width + self.kx, self.y - self.ky, self.width, self.height)
        rect = pygame.Rect(self.x - self.kx, self.y - self.ky, self.width, self.height)
        return rect

    def __getattribute__(self, item):
        """
        重写__getattribute__方法
        访问类属性时首先尝试返回自带属性,如果不存在则尝试返回child(可能为空)
        -->实现用访问属性的方法(A.child1)访问child
        """
        try:
            return super().__getattribute__(item)
        except AttributeError:
            if item in self._children:
                return self._children[item]
            else:
                # return None
                raise AttributeError('Node attribute not exist:{}.{}'.format(self.node_name, item))

    # def __setattr__(self, key, value):
    #     self.__dict__[key] = value

    def get_parent(self):
        return self._parent

    def set_parent(self, obj):
        self._parent = obj

    def child(self, name):
        if name in self._children:
            return self._children[name]
        else:
            # print('Warning: Node child not exist - {}.{}'.format(self.node_name, name))
            return None

    def get_children(self):
        return self._children

    def add_child(self, name, obj):
        self._children[name] = obj
        obj.set_parent(self)
        obj.node_name = name
        obj.level = self.level + 1

    def get_children_count(self):
        return len(self._children)

    def remove_child(self, name):
        if name in self._children:
            del self._children[name]

    def remove_self(self):
        """
        如果有父节点, 则从父节点的子节点中删除自己
        :return:
        """
        if self._parent:
            self._parent.remove_child(self.node_name)

    def clear_children(self, exception: list = ()):
        """
        清除所有子节点
        :param exception: 排除项, 子节点名称
        :return:
        """
        for child_name, child in self._children.copy().items():
            if child_name in exception:
                break
            child.set_parent(None)
            del self._children[child_name]
        # self._children = {}

    def process_ysort(self, reverse=False):
        """
        利用子节点的z值进行排序
        :return:
        """
        children = sorted(self._children.items(), key=lambda x: x[1].z, reverse=reverse)
        self.clear_children()
        for (name, node) in children:
            self.add_child(name, node)

    # def setup_from_config(self, config_file):
    #     """
    #     从config加载并设置节点
    #     :param config_file:
    #     :return:
    #     """
    #     with open(config_file, 'rb') as f:
    #         from Common.common import new_node
    #         config_item = pickle.load(f)
    #         # node_type = type(new_node(config_item.node_type))
    #         # if not isinstance(self, node_type):
    #         #     raise TypeError('config节点类型:\'{}\'与本身节点类型\'{}\'不符!'.format(str(node_type), str(type(self))))
    #     from Common.common import traverse_config_item
    #     traverse_config_item(config_item, self)

    def get_node(self, path: str):
        """
        通过节点路径获得节点
        :param path:
        :return:
        """
        nodes = path.strip('/').split('/')
        target = self
        try:
            for node in nodes:
                target = target.child(node)
        except:
            return None
        return target

    def check_event(self):
        """
        如果想要捕获全局事件, 在这个方法里实现
        :return:
        """
        # 检测pressed
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.director.match_mouse_event(PASS, MOUSE_LEFT_DOWN):
                self.is_pressed = True
                self.press_x, self.press_y = pygame.mouse.get_pos()
            if self.director.match_mouse_event(PASS, MOUSE_LEFT_RELEASE):
                self.is_pressed = False
                self.last_x, self.last_y = self.x, self.y
        if self.director.is_mouse_left_released:
            self.is_pressed = False
            self.last_x, self.last_y = self.x, self.y
        # 检测拖动
        if self.is_draggable and self.is_pressed:
            print('drag...')
            mpos = pygame.mouse.get_pos()
            dx = self.press_x - mpos[0]
            dy = self.press_y - mpos[1]
            self.x = self.last_x - dx
            self.y = self.last_y - dy

    def update(self):
        """
        更新(计算)的内容, 每一帧调用一次
        :return:
        """
        pass

    def draw(self):
        """
        渲染(绘制)的内容, 每一帧调用一次
        :return:
        """
        pass
