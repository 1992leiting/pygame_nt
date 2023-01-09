from Node.node import Node
from Node.scrollable_node import ScrollableNode
from Common.common import *
from Common.constants import *
import pygame


class ListItem(Node):
    def __init__(self):
        super().__init__()
        self.is_hover = False
        self.is_checked = False
        self.shift_x, self.shift_y = 0, 0
        self.hover_color = get_color('皇家蓝')
        self.checked_color = get_color('黄')
        self.blank_color = (0, 0, 0, 0)
        self.hover_box = pygame.Surface((100, 100))
        self.checked_box = pygame.Surface((100, 100))
        self._object = Node()

    """
    object: 每个ListItem都有一个Node类型的实体, 比如Text/Button/...
    object会显示父节点(ListView)的surface上,并且有shift_y
    """

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, obj:Node):
        self._object = obj
        self.width, self.height = obj.width, obj.height

    def check_event(self):
        if self.is_hover:
            pass

    def draw(self):
        if self.is_checked:
            self.surface.blit(self.checked_box, (self.x + self.shift_x, self.y + self.shift_y))
        if self.is_hover:
            self.surface.blit(self.hover_box, (self.x + self.shift_x, self.y + self.shift_y))
        self.object.draw()

    def update(self):
        if self.is_checked:
            if self.checked_box.get_size() != self.object.size:
                self.checked_box = pygame.Surface(self.object.size)
                self.checked_box.fill(self.checked_color)

        if self.is_hover:
            if self.hover_box.get_size() != self.object.size:
                self.hover_box = pygame.Surface(self.object.size)
                self.hover_box.fill(self.checked_color)

        # self.object.ori_x, self.object.ori_y = self.ori_x, self.ori_y
        self.object.update()


class ListView2(ScrollableNode):
    def __init__(self):
        super().__init__()
        self.width, self.height = 200, 200
        self.scroll_step = 8
        self.disp_height = 100
        self.surface = pygame.Surface((self.width, self.height))
        self.disp_surface = pygame.Surface((self.width, self.disp_height))
        self.items = []

    def setup(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.disp_surface = pygame.Surface(self.width, self.disp_height)

    def append_item(self, item):
        self.items.append(item)
        item.surface = self.disp_surface
        item.object.surface = self.surface

    # def scroll(self, px):
    #     super().scroll(px)
    #     for item in self.items:
    #         item.shift_y = self.scroll_value

    def draw(self):
        self.surface.fill((50, 50, 50))
        self.disp_surface.fill((100, 100, 0))
        for item in self.items:
            item.object.surface = self.surface
            item.draw()
        self.disp_surface.blit(self.surface, (0, self.scroll_value))
        game.director.screen.blit(self.disp_surface, (self.x, self.y))

    def update(self):
        _y = 0
        for item in self.items:
            item.object.ori_y = _y
            _y += item.object.height
            item.update()


class ListView(ScrollableNode):
    def __init__(self):
        super().__init__()
        self.width, self.height = 200, 200
        self.scroll_step = 8
        self.disp_height = 100
        self.surface = pygame.Surface((self.width, self.height))
        self.disp_surface = pygame.Surface((self.width, self.disp_height))
        self.hover_box = pygame.Surface((100, 100))

    def setup(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.disp_surface = pygame.Surface(self.width, self.disp_height)

    def add_child(self, name, obj):
        super().add_child(name, obj)
        obj.is_hover_enabled = True
        obj.visible = True

    # def append_item(self, item):
    #     self.items.append(item)
    #     item.surface = self.disp_surface
    #     item.object.surface = self.surface

    # def scroll(self, px):
    #     super().scroll(px)
    #     for item in self.items:
    #         item.shift_y = self.scroll_value

    def draw(self):
        self.surface.fill((50, 50, 50))
        self.disp_surface.fill((100, 100, 0))

        for child in self.get_children().values():
            if child.is_hover:
                self.surface.blit(self.hover_box, (0, child.ori_y))
            child.draw()
        self.disp_surface.blit(self.surface, (0, self.scroll_value))
        game.director.screen.blit(self.disp_surface, (self.x, self.y))

    def update(self):
        _y = 0
        for child in self.get_children().values():
            child.surface = self.surface
            child.ori_x = -self.x
            child.ori_y = _y - self.y
            _y += child.height

            self.hover_box = pygame.Surface((0, 0))
            if child.is_hover:
                print('child is hover:', child.node_name)
                self.hover_box = pygame.Surface((child.width, child.height))
                self.hover_box.fill(get_color('黄'))
