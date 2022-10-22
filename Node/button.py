import pygame.mouse
from Node.node import Node
from constants import *


class Button(Node):
    def __init__(self):
        super(Button, self).__init__()
        self.img_normal = None
        self.img_hover = None
        self.img_pressed = None
        self.img_disable = None
        self.cur_img = None  # 当前正在显示的image
        self.is_hover = False
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

    def update(self):
        # 判断hover
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pos = pygame.mouse.get_pos()
            rect_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
            if self.rect.collidepoint(pos):
                color = self.cur_img.get_at(rect_pos)
                self.is_hover = (color != (0, 0, 0, 0))
            else:
                self.is_hover = False
        else:
            self.is_hover = False

        # 判断按住
        if self.is_hover:
            if self.director.match_mouse_event(self.mouse_filter, MOUSE_LEFT_DOWN):
                self.is_pressed = True
            if self.is_pressed and self.director.match_mouse_event(self.mouse_filter, MOUSE_LEFT_RELEASE):
                self.is_pressed = False
        else:
            self.is_pressed = False
            self.cur_img = self.img_normal

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
