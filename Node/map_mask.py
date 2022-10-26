import pygame.draw
from Node.node import Node
import time


class MapMask(Node):
    def __init__(self):
        super(MapMask, self).__init__()
        self.x, self.y = 0, 0  # 默认为左上角坐标
        self.width, self.height = 0, 0
        self.id = 0
        self.img = None
        self.is_hover_enabled = False

    @property
    def z(self):
        return self.y + self.height

    def draw(self):
        if self.img:
            self.director.screen.blit(self.img, (self.x - self.kx, self.y - self.ky))
        # pygame.draw.circle(self.director.screen, (255, 0, 0), (self.x, self.y), 5)
        # pygame.draw.rect(self.director.screen, (255, 255, 0), self.rect, 2)
