import pygame.freetype
from Node.node import Node
from Common.constants import *


class Label(Node):
    def __init__(self, text='', color=(255, 255, 255), size=14, italic=False, shadow=False, anti_aliased=False, underline=False, bold=False, twinkle=False, font_name=DEFAULT_FONT):
        super(Label, self).__init__()
        self.font_name = font_name
        self.font = None
        self.text = text
        self.size = size
        self.shadow = shadow  # 阴影
        self.anti_aliased = anti_aliased  # 抗锯齿
        self.underline = underline  # 下划线
        if bold:
            print('Label暂时不能设置为True...')
        self.bold = False  # 加粗
        self.italic = italic  # 斜体
        self.twinkle = twinkle  # 闪烁
        self.font_surface = None
        self.shadow_surface = None
        self.color = color
        self.setup()

    def setup(self):
        self.font = pygame.freetype.Font(font_dir + self.font_name, size=self.size)
        self.font.strong = self.bold
        self.font.underline = self.underline
        self.font.oblique = self.italic
        # 抗锯齿效果有3种状态: 不设置, 设置False, 设置True, 部分字体不设置效果最好
        if self.font_name == DEFAULT_FONT:
            self.font.antialiased = self.anti_aliased
        self.font_surface, (_, _, self.width, self.height) = self.font.render(self.text, fgcolor=self.color, size=self.size)
        # 阴影效果其实是绘制两层文字, 底层会黑色且有一定位置偏移
        if self.shadow:
            shadow_label = Label(self.text, self.color, self.size, self.italic, self.anti_aliased, False, self.underline, self.bold, False, self.font_name)
            shadow_label.x = -1
            shadow_label.y = -1
            self.x += 1
            self.y += 1
            self.font_surface, (_, _, self.width, self.height) = self.font.render(self.text, fgcolor=(0, 0, 0), size=self.size)
            self.add_child('shadow', shadow_label)
        self.width = self.rect[2]
        self.height = self.rect[3]

    def draw(self):
        self.director.screen.blit(self.font_surface, (self.x, self.y))
