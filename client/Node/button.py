import pygame.mouse
from Node.node import Node
from Common.constants import *
from Game.res_manager import fill_button
from Node.label import Label


class Button(Node):
    def __init__(self):
        super(Button, self).__init__()
        self.is_active = True  # 是否使能状态
        self.img_normal = None
        self.img_hover = None
        self.img_pressed = None
        self.img_disable = None
        self.cur_img = None  # 当前正在显示的image
        self.is_pressed = False
        self.is_locked = False
        self.toggle_mode = False  # 按下锁定模式
        self.is_toggled = False
        self.toggle_button_group = None  # toggle按钮组
        self._event = None
        self.mouse_filter = STOP
        self.is_single_frame = False  # 是否是单帧素材按钮
        self.rsp_file = ''
        self.hash_id = 0

    @property
    def event(self):
        """
        当外部访问event时, 会返回_event并清空_event
        :return:
        """
        _tmp = self._event
        self._event = None
        return _tmp

    def setup(self):
        if self.rsp_file and self.hash_id:
            fill_button(self, self.rsp_file, self.hash_id)

    def check_hover(self):
        if self.director.node_hover is None and self.rect.collidepoint(pygame.mouse.get_pos()):
            pos = pygame.mouse.get_pos()
            rect_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
            if self.rect.collidepoint(pos):
                if self.cur_img:
                    color = self.cur_img.get_at(rect_pos)
                    if color != (0, 0, 0, 0):
                        self.director.node_hover = self
                        self.is_hover = True
                else:
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
        if not self.is_active:
            return
        # 判断按住
        if self.is_hover:
            if self.director.match_mouse_event(STOP, MOUSE_LEFT_DOWN):
                self.is_pressed = True
                if self.toggle_mode:
                    self.is_toggled = True
                    self._event = True
                # 按钮组相关操作
                if self.toggle_button_group:
                    # 一个按钮按下时, 按钮组其他按钮弹起
                    self.toggle_button_group.set_toggled_button(self)
                    # for btn in self.toggle_button_group.buttons:
                    #     if btn != self:
                    #         btn.is_toggled = False
            if self.is_pressed and self.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
                self.is_pressed = False
                if not self.is_toggled:
                    self._event = True
        else:
            self.is_pressed = False
            if not self.is_toggled:
                self.cur_img = self.img_normal

    def update(self):
        self.cur_img = self.img_normal
        if self.is_hover:
            self.cur_img = self.img_hover
        if self.is_pressed:
            self.cur_img = self.img_pressed
        if self.is_toggled:
            self.cur_img = self.img_pressed
        if not self.is_active:
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
    def __init__(self, text='按钮', width=800):
        super(ButtonClassicRed, self).__init__()
        fill_button(self, 'wzife4.rsp', 0x0267FB16)
        self.text = text
        self.width = width
        self.setup()

    def setup(self):
        self.auto_sizing()
        self.x -= 5
        self.y -= 5
        label = Label(self.text, size=14)
        label.center_x = self.width/2
        label.center_y = self.height/2
        self.add_child('label', label)
        label.is_hover_enabled = False


class ToggleButtonGroup(Node):
    """
    锁定按钮组, 只允许有一个按钮处于锁定状态
    """
    def __init__(self):
        super(ToggleButtonGroup, self).__init__()
        self.buttons = []
        self.toggled_button = None  # 当前锁定的按钮序号

    def append(self, btn):
        self.buttons.append(btn)
        btn.toggle_button_group = self

    def set_toggled_button(self, btn):
        for i, button in enumerate(self.buttons):
            if button == btn:
                self.toggled_button = i
            else:
                button.is_toggled = False

    def update(self):
        # 默认第一个按钮锁定
        if self.buttons and self.toggled_button is None:
            print('默认0')
            self.toggled_button = 0
        if self.buttons:
            self.buttons[self.toggled_button].is_toggled = True


class DialogOptionItem(Button):
    def __init__(self, text):
        super(DialogOptionItem, self).__init__()
        self.text = text
        fill_button(self, 'wzife4.rsp', 0x802EB60A)
        self.setup()

    def setup(self):
        label = Label(self.text, size=15, color=(255, 0, 0))
        self.add_child('label', label)
        label.ori_x, label.ori_y = 10, 6
        label.is_hover_enabled = False
        self.width = label.width + 20
        self.auto_sizing()
        self.img_normal = None  # 不指向时不显示背景
