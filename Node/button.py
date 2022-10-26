import pygame.mouse
from Node.node import Node
from Common.constants import *
from Game.res_manager import fill_button


class Button(Node):
    def __init__(self):
        super(Button, self).__init__()
        self.img_normal = None
        self.img_hover = None
        self.img_pressed = None
        self.img_disable = None
        self.cur_img = None  # 当前正在显示的image
        self.is_pressed = False
        self.is_locked = False
        self._event = None
        self.mouse_filter = STOP
        self.is_single_frame = False  # 是否是单帧素材按钮

    @property
    def event(self):
        """
        当外部访问event时, 会返回_event并清空_event
        :return:
        """
        _tmp = self._event
        self._event = None
        return _tmp

    def check_hover(self):
        # 判断hover
        # if self.director.node_hover is not None:
        #     self.is_hover = False
        #     return
        if self.director.node_hover is None and self.rect.collidepoint(pygame.mouse.get_pos()):
            pos = pygame.mouse.get_pos()
            rect_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
            if self.rect.collidepoint(pos):
                color = self.cur_img.get_at(rect_pos)
                if color != (0, 0, 0, 0):
                    self.director.node_hover = self
                    self.is_hover = True
            else:
                self.is_hover = False
        else:
            self.is_hover = False

    def auto_sizing(self):
        from Common.common import auto_sizing
        self.img_normal = auto_sizing(self.img_normal, self.width, self.height)
        self.img_pressed = auto_sizing(self.img_pressed, self.width, self.height)
        self.img_hover = auto_sizing(self.img_hover, self.width, self.height)
        self.img_disable = auto_sizing(self.img_disable, self.width, self.height)

    def check_event(self):
        # super(Button, self).check_event()

        # 判断按住
        if self.is_hover:
            if self.director.match_mouse_event(STOP, MOUSE_LEFT_DOWN):
                self.is_pressed = True
            if self.is_pressed and self.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                self.is_pressed = False
                self._event = True
        else:
            self.is_pressed = False
            self.cur_img = self.img_normal

    def update(self):
        self.cur_img = self.img_normal
        if self.is_hover:
            self.cur_img = self.img_hover
        if self.is_pressed:
            self.cur_img = self.img_pressed
        if not self.enable:
            self.cur_img = self.img_disable

    def draw(self):
        if self.cur_img:
            # 单帧按钮按下时偏移1个像素模拟按下效果
            if self.is_pressed and self.is_single_frame:
                self.director.screen.blit(self.cur_img, (self.x + 1, self.y + 1))
            else:
                self.director.screen.blit(self.cur_img, (self.x, self.y))
        # pygame.draw.rect(self.director.screen, (255, 255, 255), self.rect, 1)


class ButtonClassicClose(Button):
    """
    传统样式关闭按钮
    """
    def __init__(self):
        super(ButtonClassicClose, self).__init__()
        fill_button(self, 'wzife.rsp', 0xF11233BB)

    def check_event(self):
        super(ButtonClassicClose, self).check_event()
        if self.event and self.get_parent():
            print('close event')
            self.get_parent().visible = False


class ButtonClassicRed(Button):
    """
    传统样式红色按钮
    """
    def __init__(self, text, width):
        super(ButtonClassicRed, self).__init__()
        fill_button(self, 'wzife4.rsp', 0x0267FB16)
        self.text = text
        self.width = width
        self.setup()

    def setup(self):
        self.auto_sizing()
        from Node.label import Label
        label = Label(self.text, size=14)
        label.center_x = self.center_x
        label.center_y = self.center_y
        self.add_child('label', label)
        label.is_hover_enabled = False
