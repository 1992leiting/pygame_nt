import time

import pygame
from Node.node import Node
from Common.constants import *
from Node.rich_text import Word
from Common.common import get_color
from Node.image_rect import ImageRect
from Game.res_manager import fill_image_rect


class TextEditManager:
    def __init__(self):
        self.edit_group = []

    @property
    def active_edit(self):
        for edit in self.edit_group:
            if edit.is_active:
                return edit
        return None

    def append(self, edit):
        self.edit_group.append(edit)

    def activate(self, edit):
        for e in self.edit_group:
            e.is_active = (e == edit)

    def deactivate(self, edit):
        for e in self.edit_group:
            if e == edit:
                e.is_active = False


class LineEdit(Node):
    def __init__(self, text='', width=800, font_size=14, font_name=DEFAULT_FONT, font_color='白'):
        super(LineEdit, self).__init__()
        self.text = text
        self.width, self.height = width, font_size
        self.font_size = font_size
        self.font_name = font_name
        self.surface = pygame.Surface((self.width, self.height))
        self.is_active = False
        self.is_readonly = False  # 只读
        self.lines = 1  # 设定的行数
        self.word_space = 1  # 字间距
        self.line_space = 1  # 行间距
        self.dx, self.dy = 0, 0  # 文本基于surface左上角偏移的坐标(用于边角留白)
        self.shift_x, self.shift_y = 0, 0  # 文字的偏移量(溢出时起作用)
        self.word_list = []
        self.text_color = get_color(font_color)
        self.italic = False
        self.shadow = False
        self.password_mode = False  # 密码模式
        self.tk_timer = 0  # 闪烁计时器
        self.cursor_pos = 0  # 光标的位置(第几个字符的右边)
        self.cursor_x, self.cursor_y = 0, 0  # 光标坐标
        self._enter_event = None

    @property
    def enter_event(self):
        """
        当外部访问event时, 会返回_event并清空_event
        :return:
        """
        _tmp = self._enter_event
        self._enter_event = None
        return _tmp

    def setup(self):
        self.height = self.font_size
        if self.director.te_manager is None:
            self.director.te_manager = TextEditManager()
        self.director.te_manager.append(self)
        self._parse()

    def insert_text(self, txt: str):
        if len(txt) <= 0:
            return
        ori = list(self.text)  # 原始文本, 在此基础上插入
        new = list(txt)
        for i in range(len(new)):
            ori.insert(self.cursor_pos, new[i])
            self.cursor_pos += 1
        self.text = ''.join(map(str, ori))
        self._parse()

    def delete_text(self, direction=0):
        if len(self.text) <= 0:
            return
        if self.cursor_pos == 0:
            return
        ori = list(self.text)
        try:
            ori.pop(self.cursor_pos - 1)
            self.cursor_pos -= 1
            self.text = ''.join(map(str, ori))
            self._parse()
        except:
            pass

    def set_text(self, text):
        if str(text) != str(self.text):
            self.text = text
            self._parse()

    def clear_text(self):
        self.text = ''
        self._parse()

    def _parse(self):
        self.text = str(self.text)
        self.word_list = []
        self.surface = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        cur_width = 0  # 当前行字符显示的宽度
        char_list = list(self.text)
        for i in range(len(char_list)):
            ch = char_list[i]
            if self.password_mode:
                ch = '*'
            self.word_list.append(Word(ch, size=self.font_size, color=self.text_color))
        _sx, _sy = 0, 0  # 当前字符显示坐标(基于self.surface左上角)
        # 解析每一个字符
        for i, word in enumerate(self.word_list):
            _sx = self.dx + cur_width
            char_width = word.width
            word.x, word.y = _sx + self.shift_x, _sy + (self.font_size - word.height)  # 底部对齐
            word.render_to(self.surface, word.x, word.y)
            cur_width = cur_width + char_width + self.word_space

    def update(self):
        if self.is_readonly:
            self.is_active = False
        # 鼠标指向时指针变化
        else:
            if self.is_hover:
                if self.director.te_hover != self:
                    self.director.te_hover = self
                    self.director.child('mouse').change_state('输入')
            else:
                if self.director.te_hover == self:
                    self.director.te_hover = None
                    self.director.child('mouse').set_last_state()

        # 光标坐标
        self.cursor_x = 0
        for i in range(self.cursor_pos):
            if i < len(self.word_list):
                self.cursor_x += self.word_list[i].width + self.word_space

        # x方向光标溢出
        if self.cursor_x > self.width:
            self.shift_x = self.width - self.cursor_x
            self.cursor_x = self.width
            self._parse()
        else:
            if self.shift_x != 0:
                self.shift_x = 0
                self._parse()

    def draw(self):
        self.director.screen.blit(self.surface, (self.x, self.y))
        # active状态下闪烁光标
        if self.is_active:
            if time.time() - self.tk_timer > 0.8:
                pygame.draw.line(self.director.screen, self.text_color, (self.cursor_x + self.x, self.cursor_y + self.y), (self.cursor_x + self.x, self.cursor_y + self.font_size + self.y), width=1)
            if time.time() - self.tk_timer > 1.6:
                self.tk_timer = time.time()

    def check_event(self):
        super(LineEdit, self).check_event()

        # 点击激活
        if not self.is_readonly:
            if self.is_hover:
                if self.director.match_mouse_event(self.mouse_filter, MOUSE_LEFT_DOWN):
                    self.director.te_manager.activate(self)

            if self.is_active:
                if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_BACKSPACE]):
                    self.delete_text()
                self.insert_text(self.director.get_kb_text())
                if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_LEFT]):
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_RIGHT]):
                    self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
        if self.is_active:
            if self.director.match_kb_event(STOP, pygame.K_KP_ENTER) or self.director.match_kb_event(STOP, pygame.K_RETURN):
                self._enter_event = True


class TextEdit(LineEdit):
    def __init__(self, text='', width=200, height=200, font_size=14, font_name=DEFAULT_FONT, text_color='白'):
        super(TextEdit, self).__init__()
        self.text = text
        self.width, self.height = width, height
        self.font_size = font_size
        self.font_name = font_name
        self.surface = pygame.Surface((self.width, self.height))
        self.is_active = False
        self.lines = 1  # 设定的行数
        self.word_space = 1  # 字间距
        self.line_space = 1  # 行间距
        self.dx, self.dy = 0, 0  # 文本基于surface左上角偏移的坐标(用于边角留白)
        self.shift_x, self.shift_y = 0, 0  # 文字的偏移量(溢出时起作用)
        self.word_list = []
        self.text_color = get_color(text_color)
        self.italic = False
        self.shadow = False
        self.password_mode = False  # 密码模式
        self.tk_timer = 0  # 闪烁计时器
        self.cursor_pos = 0  # 光标的位置(第几个字符的右边)
        self.cursor_x, self.cursor_y = 0, 0  # 光标坐标
        if self.director.te_manager is None:
            self.director.te_manager = TextEditManager()
        self.director.te_manager.append(self)
        self._parse()

    def _parse(self):
        self.word_list = []
        self.surface = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        cur_width = 0  # 当前行字符显示的宽度
        char_list = list(self.text)
        for i in range(len(char_list)):
            ch = char_list[i]
            if self.password_mode:
                ch = '*'
            self.word_list.append(Word(ch, color=self.text_color))
        _sx, _sy = 0, 0  # 当前字符显示坐标(基于self.surface左上角)
        # 解析每一个字符
        for i, word in enumerate(self.word_list):
            _sx = self.dx + cur_width
            char_width = word.width
            word.x, word.y = _sx + self.shift_x, _sy + (self.font_size - word.height)  # 底部对齐
            cur_width = cur_width + char_width + self.word_space
            if cur_width > self.width:
                cur_width = 0
                _sx = 0
                _sy = _sy + self.font_size + self.line_space
                word.x, word.y = _sx + self.shift_x, _sy + (self.font_size - word.height)  # 底部对齐
                cur_width = cur_width + char_width + self.word_space
            word.render_to(self.surface, word.x, word.y)

    def check_event(self):
        super(TextEdit, self).check_event()
        # 鼠标指向时指针变化
        if self.is_hover:
            if self.director.te_hover != self:
                self.director.te_hover = self
                self.director.child('mouse').change_state('输入')
        else:
            if self.director.te_hover == self:
                self.director.te_hover = None
                self.director.child('mouse').set_last_state()

        # 点击激活
        if self.is_hover:
            if self.director.match_mouse_event(self.mouse_filter, MOUSE_LEFT_DOWN):
                self.director.te_manager.activate(self)

    def update(self):
        # 光标坐标
        self.cursor_x = 0
        for i in range(self.cursor_pos):
            if i < len(self.word_list):
                # self.cursor_x += self.word_list[i].width + self.word_space
                self.cursor_x = self.word_list[i].x + self.word_list[i].width
                self.cursor_y = self.word_list[i].y - (self.font_size - self.word_list[i].height)

        # x方向光标溢出
        # if self.cursor_x > self.width:
        #     self.shift_x = self.width - self.cursor_x
        #     self.cursor_x = self.width
        #     self._parse()
        # else:
        #     if self.shift_x != 0:
        #         self.shift_x = 0
        #         self._parse()


class LineEditWithBg(ImageRect):
    def __init__(self, width=800, text=''):
        super(LineEditWithBg, self).__init__()
        fill_image_rect(self, 'wzife4.rsp', 0xB74E6CA1)  # 圆角输入背景
        self.width = width
        self.font_size = 15
        self.line_edit = LineEdit(font_color='黑')
        self.line_edit.is_readonly = True
        self.setup()

    @property
    def text(self):
        return self.line_edit.text

    @property
    def y(self):
        if self._parent:
            return self.ori_y + self._parent.y
        else:
            return self.ori_y

    @y.setter
    def y(self, yy):
        if self._parent:
            self.ori_y = yy - self._parent.y - 4
        else:
            self.ori_y = yy - 4

    @text.setter
    def text(self, txt):
        self.line_edit.text = txt
        self.line_edit.setup()

    @property
    def is_readonly(self):
        return self.line_edit.is_readonly

    @is_readonly.setter
    def is_readonly(self, v):
        self.line_edit.is_readonly = v

    def set_text(self, text):
        if str(text) != str(self.text):
            self.text = text
            self.setup()

    def setup(self):
        self.auto_sizing(w=self.width)
        self.line_edit.text = self.text
        self.line_edit.font_size = self.font_size
        self.line_edit.width = self.width - 14
        self.line_edit.x = self.x + 8
        self.line_edit.y = self.y + 2
        self.line_edit.setup()
        self.add_child('edit', self.line_edit)
