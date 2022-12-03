from Node.animation import Animation
import pygame
from Common.constants import *


class Emoji(Animation):
    def __init__(self):
        super(Emoji, self).__init__()
        self.mouse_filter = STOP
        self.shift_x, self.shift_y = 0, 0
        self.id = 0

    @property
    def rect(self):
        rect = pygame.Rect(self.x + self.shift_x, self.y - self.ky + self.shift_y, self.width, self.height)
        return rect

    def draw(self):
        if self.cur_frame:
            _frame = self.cur_frame.copy()
            self.surface.blit(_frame, (self.x, self.ori_y - self.ky + self.shift_y))
        # pygame.draw.rect(self.surface, (255, 255, 255), self.rect, 1)
        # pygame.draw.circle(self.surface, (255, 0, 0), (self.x, self.y), 4)

    def check_event(self):
        super(Emoji, self).check_event()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.director.match_mouse_event(self.mouse_filter, MOUSE_LEFT_DOWN):
                print('emoji:', self.id)
