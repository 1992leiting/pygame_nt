import time

import pygame
from Common.common import *
from Node.node import Node
from Node.label import Label
from Common.constants import *
from Node.emoji import Emoji


class Word:
    def __init__(self, char, color=(255, 255, 255), size=14, italic=False, shadow=False, anti_aliased=False, underline=False, bold=False, twinkle=False, font_name=DEFAULT_FONT, h_center=False):
        self.font_name = font_name
        self.font = None
        self.char = str(char)
        self.size = size
        self.shadow = shadow  # 阴影
        self.anti_aliased = anti_aliased  # 抗锯齿
        self.underline = underline  # 下划线
        self.bold = bold  # 加粗
        self.italic = italic  # 斜体
        self.twinkle = twinkle  # 闪烁
        self.font_surface = None
        self.shadow_surface = None
        self.color = color
        self.width_offset = 0
        self.height_offset = 0
        self.x, self.y = 0, 0  # 要显示的位置
        self.h_center_aligned = h_center  # 上下居中(只针对数字)

        # print('word:size:', self.size, self.char)
        self.font = pygame.freetype.Font(font_dir + self.font_name, size=self.size)
        self.font.strong = self.bold
        self.font.underline = self.underline
        self.font.oblique = self.italic
        # 抗锯齿效果有3种状态: 不设置, 设置False, 设置True, 部分字体不设置效果最好
        if self.font_name == DEFAULT_FONT:
            self.font.antialiased = self.anti_aliased
            if self.char in ['/', '\\', '#', '^']:
                self.font.antialiased = True
        # 直接render单个文字其宽度高度会是实际字形的宽高, 所以render时加一个空格, 计算宽度时补偿一下空格的宽度
        _, (_, _, self.width_offset, _) = self.font.render(' ', fgcolor=self.color, size=self.size)
        self.font_surface, (_, _, self.width, self.height) = self.font.render(' ' + self.char, fgcolor=self.color, size=self.size)
        self.width -= self.width_offset  # 补偿一个空格的宽度
        # 数字垂直居中显示, 要计算高度并补偿
        if self.h_center_aligned and self.char.isdigit():
            _, (_, _, _, word_height) = self.font.render(self.char, fgcolor=self.color, size=self.size)
            self.height_offset += (self.size - word_height)//2  # 上下居中
        # 不垂直居中显示的话字母和数字上抬
        else:
            if self.char.isdigit() or self.char in ALPHABET:
                self.height_offset += int(self.size/10)
        # 阴影效果其实是绘制两层文字, 底层会黑色且有一定位置偏移
        if self.shadow:
            self.shadow_surface, (_, _, self.width, self.height) = self.font.render(' ' + self.char, fgcolor=(0, 0, 0), size=self.size)

    def render_to(self, surf: pygame.Surface, x, y):
        surf.blit(self.font_surface, (x - self.width_offset, y - self.height_offset))


class RichText(Node):
    def __init__(self, text='', width=200, height=200, font_size=14, font_name=DEFAULT_FONT, h_center=False):
        super(RichText, self).__init__()
        self.text = text  # 所有文本内容
        self.word_list = []  # 文本内容会转换为单个字符
        self.total_line_num = 0  # 总的行数
        self.word_space = 0  # 字间距
        self.line_space = 1  # 行间距
        self.font_size = font_size  # 字体大小
        self.font_name = font_name  # 字体名称
        self.dx, self.dy = 0, 0  # 文本基于surface左上角偏移的坐标
        self.width, self.height = width, height
        self.actual_width = 0  # 实际宽度,如果没满一行,实际宽度可能<self.width,如果多余一行则=self.width
        self.max_height = self.height  # 解析之后获得的最大高度值(用于调整dynamic/static_surface大小)
        self.surface = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)  # 显示内容的surface
        self.static_surface = pygame.Surface((self.width, self.max_height), flags=pygame.SRCALPHA)  # 显示静态元素的surface，如文字
        self.dynamic_surface = pygame.Surface((self.width, self.max_height), flags=pygame.SRCALPHA)  # 显示动态元素的surface，如emoji
        self._cnt = 0
        self.scroll = 0  # 纵向滚动的像素数量
        self.h_center_aligned = h_center # 上下居中,只针对数字
        self._parse()
        
    @property
    def cnt(self):
        self._cnt += 1
        return self._cnt

    def set_text(self, text):
        self.text = text
        self._parse()

    def append_text(self, text):
        self.text = self.text + '\n' + text
        self._parse()

    def _parse(self):
        """
        解析所有富文本内容, 根据内容生成静态(文字)和动态(emoji)元素
        :return:
        """
        char_list = list(self.text)  # 将字符串转换为列表
        self.word_list = []
        color = (255, 255, 255)  # 默认白色
        ul_flag = False  # 下划线标志位
        bd_flag = False  # 加粗标志位
        tk_flag = False  # 闪烁标志位
        it_flag = False  # 斜体标志位
        skip = 0
        for i in range(len(char_list)):
            if skip > 0:  # 遇到特殊格式时, 需要跳过一个字符
                skip -= 1
                continue
            if char_list[i] == '#' and i < len(char_list) - 1 and char_list[i + 1] in MY_COLOR:  # 置颜色
                # 遇到新的颜色则重置下划线/加粗/闪烁为False
                color = get_color(char_list[i + 1])
                ul_flag = False
                bd_flag = False
                tk_flag = False
                skip = 1
            elif char_list[i] == '#' and i < len(char_list) - 1 and char_list[i + 1] == 'u':  # 置下划线
                ul_flag = True
                skip = 1
            elif char_list[i] == '#' and i < len(char_list) - 1 and char_list[i + 1] == 'b':  # 置加粗
                bd_flag = True
                skip = 1
            elif char_list[i] == '#' and i < len(char_list) - 1 and char_list[i + 1] == 't':  # 置闪烁
                tk_flag = True
                skip = 1
            elif char_list[i] == '#' and i < len(char_list) - 1 and char_list[i + 1] == 'i':  # 置斜体
                it_flag = True
                skip = 1
            elif char_list[i] == '#':
                # 梦幻表情包
                if i < len(char_list) - 1 and char_list[i + 1] in '0123456789':
                    emoji_index = None
                    emoji_index = int(char_list[i + 1])
                    skip = 1
                    if i < len(char_list) - 2 and char_list[i + 2] in '0123456789':
                        emoji_index = emoji_index * 10 + int(char_list[i + 2])
                        skip = 2
                        if i < len(char_list) - 3 and char_list[i + 3] in '0123456789':
                            emoji_index = emoji_index * 10 + int(char_list[i + 3])
                            skip = 3
                    if emoji_index is not None:
                        from Game.res_manager import fill_res
                        emoji = Emoji()
                        emoji.surface = self.dynamic_surface
                        fill_res(emoji, 'wzife.rsp', MY_EMOJI[emoji_index])
                        self.word_list.append(emoji)
                # 频道图片
                chl_name = None
                if i < len(char_list) - 2 and (char_list[i + 1] + char_list[i + 2]) == 'xt':
                    chl_name = 'xt'
                elif i < len(char_list) - 2 and (char_list[i + 1] + char_list[i + 2]) == 'sj':
                    chl_name = 'sj'
                elif i < len(char_list) - 2 and (char_list[i + 1] + char_list[i + 2]) == 'dq':
                    chl_name = 'dq'
                elif i < len(char_list) - 2 and (char_list[i + 1] + char_list[i + 2]) == 'sl':
                    chl_name = 'sl'
                elif i < len(char_list) - 2 and (char_list[i + 1] + char_list[i + 2]) == 'gm':
                    chl_name = 'gm'
                elif i < len(char_list) - 2 and (char_list[i + 1] + char_list[i + 2]) == 'cw':
                    chl_name = 'cw'
                elif i < len(char_list) - 2 and (char_list[i + 1] + char_list[i + 2]) == 'bp':
                    chl_name = 'bp'
                elif i < len(char_list) - 2 and (char_list[i + 1] + char_list[i + 2]) == 'dw':
                    chl_name = 'dw'
                if chl_name is not None:
                    print('频道emoji:', chl_name)
                    skip = 2
                    from Game.res_manager import fill_res
                    emoji = Emoji()
                    emoji.surface = self.dynamic_surface
                    fill_res(emoji, 'wzife.rsp', CHL_EMOJI[chl_name])
                    emoji.shift_y = 1
                    self.word_list.append(emoji)
            else:
                char = char_list[i]
                if char == '\n':  # 换行符替换一下避免一些错误
                    char = '#n'
                self.word_list.append(Word(char, color=color, underline=ul_flag, bold=bd_flag, twinkle=tk_flag, size=self.font_size, font_name=self.font_name, h_center=self.h_center_aligned))
        self.compose()

    def compose(self):
        """
        对已经解析好的内容进行排版
        :return:
        """
        self.static_surface = pygame.Surface((self.width, self.max_height), flags=pygame.SRCALPHA)
        self.dynamic_surface = pygame.Surface((self.width, self.max_height), flags=pygame.SRCALPHA)
        self.dynamic_surface.fill((0, 0, 0, 0))
        self.surface.fill((0, 0, 0, 0))
        self.total_line_num = 1
        cur_line_num = 1  # 当前第几行
        cur_width = 0  # 当前行宽度累加值
        cur_line_height = self.font_size  # 当前行的高度(取最大值)
        cur_line_words = []  # 当前行的字符或表情, 暂存然后换行时一起设置
        _sx, _sy = 0, 0  # 当前字符显示坐标(基于self.surface左上角)
        # 解析每一个字符
        for i, word in enumerate(self.word_list):
            if type(word) == Word:  # 解析到字符
                # 遇到换行符则换行
                if word.char == '#n':
                    cur_line_num += 1
                    cur_width = 0
                    for w in cur_line_words:
                        if type(w) == Word:  # 文字
                            w.render_to(self.static_surface, w.x, _sy + (self.font_size - w.height) + (cur_line_height - self.font_size))
                        elif type(w) == Emoji:  # emoji
                            w.y = _sy + cur_line_height
                            # self.add_child(str(self.cnt), w)
                    _sy += (cur_line_height + self.line_space)
                    cur_line_height = self.font_size
                    cur_line_words = []
                    continue
                _sx = self.dx + cur_width
                char_with = word.width
                word.x, word.y = _sx, _sy + (self.font_size - word.height)
            elif type(word) == Emoji:  # 解析到表情
                _sx = self.dx + cur_width
                char_with = word.width
                word.x, word.y = _sx, _sy + word.height
            cur_line_words.append(word)
            cur_line_height = max(cur_line_height, word.height)
            cur_width = cur_width + char_with + self.word_space
            # 行宽度满且不是最后一个字符则换行
            if cur_width + self.word_space + self.font_size > self.width:
                if i != len(self.word_list)-1:
                    cur_line_num += 1
                    cur_width = 0
                    for w in cur_line_words:
                        if type(w) == Word:
                            w.render_to(self.static_surface, w.x, _sy + (self.font_size - w.height) + (cur_line_height - self.font_size))
                        elif type(w) == Emoji:
                            w.y = _sy + cur_line_height
                            # self.add_child(str(self.cnt), w)
                    _sy += (cur_line_height + self.line_space)
                    cur_line_height = self.font_size
                    cur_line_words = []
            self.total_line_num = max(self.total_line_num, cur_line_num)

        # 最后一行
        if len(cur_line_words) > 0:
            for w in cur_line_words:
                if type(w) == Word:
                    w.render_to(self.static_surface, w.x, _sy + (self.font_size - w.height) + (cur_line_height - self.font_size))
                elif type(w) == Emoji:
                    w.y = _sy + cur_line_height
                    # self.add_child(str(self.cnt), w)

        self.max_height = _sy + cur_line_height
        if self.max_height > self.dynamic_surface.get_height() or self.max_height > self.static_surface.get_height():
            self.static_surface = pygame.Surface((self.width, self.max_height), flags=pygame.SRCALPHA)
            self.dynamic_surface = pygame.Surface((self.width, self.max_height), flags=pygame.SRCALPHA)
            self.compose()

        # 实际宽度
        if self.total_line_num < 2:
            self.actual_width = cur_width
        else:
            self.actual_width = self.width

    def draw(self):
        self.surface.fill((0, 0, 0, 0))
        self.dynamic_surface.fill((0, 0, 0, 0))
        # 手动控制emoji的update并显示在dynamic_surface上
        for word in self.word_list:
            if type(word) == Emoji:
                word.update()
                if word.cur_frame:
                    _frame = word.cur_frame.copy()
                    self.dynamic_surface.blit(_frame, (word.x, word.y - word.ky + word.shift_y))
        self.surface.blit(self.dynamic_surface, (0, self.scroll))
        self.surface.blit(self.static_surface, (0, self.scroll))
        self.director.screen.blit(self.surface, (self.x, self.y))

    def check_event(self):
        super(RichText, self).check_event()

        if self.is_hover:
            s = self.director.get_mouse_scroll(self.mouse_filter) * 8  # 鼠标滚动转换为滚动像素数量
            if s:
                self.scroll += s
                # 设置滚动像素的上下限
                if self.scroll > 0:
                    self.scroll = 0
                if self.scroll < -self.max_height + self.height:
                    self.scroll = -self.max_height + self.height
                self.surface = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
