import pygame.freetype
from Node.node import Node
from Common.constants import *


class Label(Node):
    def __init__(self, text='', color=(255, 255, 255), size=14, italic=False, shadow=False, anti_aliased=False, underline=False, bold=False, twinkle=False, font_name=DEFAULT_FONT, outline=False):
        super(Label, self).__init__()
        self.font_name = font_name
        self.font = None
        self.text = str(text)
        self.font_size = size
        self.shadow = shadow  # 阴影
        self.anti_aliased = anti_aliased  # 抗锯齿
        self.underline = underline  # 下划线
        self.outline = outline  # 轮廓
        self.bold = bold  # 加粗
        self.italic = italic  # 斜体
        self.twinkle = twinkle  # 闪烁
        self.font_surface = None
        self.shadow_surface = None
        self.color = color
        self.setup()

    def set_text(self, text):
        if str(text) != self.text:
            self.text = text
            self.setup()

    def setup(self):
        self.clear_children()
        # outline和shadow不共存
        if self.outline:
            self.shadow = False
        self.font = pygame.freetype.Font(font_dir + self.font_name, size=self.font_size)
        self.font.strong = self.bold
        self.font.underline = self.underline
        self.font.oblique = self.italic
        # 抗锯齿效果有3种状态: 不设置, 设置False, 设置True, 部分字体不设置效果最好
        if self.font_name == DEFAULT_FONT:
            self.font.antialiased = self.anti_aliased
        self.font_surface, (_, _, self.width, self.height) = self.font.render(self.text, fgcolor=self.color, size=self.font_size)
        # 阴影效果其实是绘制两层文字, 底层会黑色且有一定位置偏移
        if self.shadow:
            # 自身作为底层阴影
            self.font_surface, (_, _, self.width, self.height) = self.font.render(self.text, fgcolor=(0, 0, 0), size=self.font_size)
            self.x += 1
            self.y += 1
            # 添加一个子label作为上层显示的label
            front_label = Label(self.text, self.color, self.font_size, self.italic, self.anti_aliased, False, self.underline, self.bold, False, self.font_name)
            front_label.ori_x = -1
            front_label.ori_y = -1
            self.add_child('front', front_label)
        # outline则是添加4层文字
        if self.outline:
            # 自身作为底层阴影
            self.font_surface, (_, _, self.width, self.height) = self.font.render(self.text, fgcolor=(0, 0, 0), size=self.font_size)
            self.x += 1
            self.y += 1
            # 再添加3层阴影
            behind_label1 = Label(self.text, (0, 0, 0), self.font_size, self.italic, self.anti_aliased, False, self.underline,
                                  self.bold, False, self.font_name)
            behind_label1.ori_x = -1
            behind_label1.ori_y = -1
            self.add_child('behind1', behind_label1)
            behind_label2 = Label(self.text, (0, 0, 0), self.font_size, self.italic, self.anti_aliased, False,
                                  self.underline, self.bold, False, self.font_name)
            behind_label2.ori_x = -1
            behind_label2.ori_y = 1
            self.add_child('behind2', behind_label2)
            behind_label3 = Label(self.text, (0, 0, 0), self.font_size, self.italic, self.anti_aliased, False,
                                  self.underline, self.bold, False, self.font_name)
            behind_label3.ori_x = 1
            behind_label3.ori_y = -1
            self.add_child('behind3', behind_label3)
            # 添加前景label
            front_label = Label(self.text, self.color, self.font_size, self.italic, self.anti_aliased, False, self.underline,
                                self.bold, False, self.font_name)
            self.add_child('front', front_label)

        self.width = self.rect[2]
        self.height = self.rect[3]

    def draw(self):
        self.surface.blit(self.font_surface, (self.x, self.y))
