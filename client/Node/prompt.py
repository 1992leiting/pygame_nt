from Node.node import Node
from Node.image_rect import ImageRect
from Node.rich_text import RichText
import time
from Common.constants import *
import pygame
from Node.label import Label
from Common.common import *
from Common.constants import *
from Node.rich_text import RichText
from Game.res_manager import fill_image_rect


class PromptManager(ImageRect):
    """
    弹出管理器,计算位置,超时消失,等
    """
    def __init__(self, style=GAME_PROMPT, x=300, y=300):
        super(PromptManager, self).__init__()
        self.x, self.y = x, y
        self.is_hover_enabled = False
        self.is_draggable = False
        self.rsp_file = 'wzife.rsp'
        self.hash_id = 0x4CFB6A98
        self.style = style
        if self.style == GAME_PROMPT:
            self.start_x, self.start_y = self.x, self.y
            self.setup()
        else:
            self.start_x, self.start_y = 0, 0
        self.x, self.y = self.start_x - self.width - 2, self.start_y - self.height - 2

    def append(self, text):
        print('添加提示:', text)
        new_pt = GamePrompt(text, style=self.style)
        new_pt.setup()
        self.add_child(new_pt.uuid, new_pt)
        self.compose()

    def compose(self):
        pt_list = list(self.get_children().copy().values())
        pt_list.reverse()
        _x, _y = self.start_x, self.start_y
        for i in range(0, len(pt_list)):
            pt = pt_list[i]
            _y = _y - PROMPT_Y_SPACE[self.style] - pt.height + 3
            if self.style == CHAR_SPEECH:
                pt.ori_y = _y
            else:
                pt.x, pt.y = _x, _y

    def check_event(self):
        super(PromptManager, self).check_event()
        self.visible = self._children

    def update(self):
        super(PromptManager, self).update()
        # 删除过期提示
        for name, child in self.get_children().copy().items():
            if time.time() - child.time > PROMPT_TIMEOUT[self.style]:
                self.remove_child(name)
                self.compose()


class GamePrompt(ImageRect):
    """
    系统提示
    """
    def __init__(self, txt='默认提示...', style=GAME_PROMPT, x=0, y=0, font_size=14):
        super(GamePrompt, self).__init__()
        print('prompt item:', txt)
        self.time = time.time()
        self.text = txt
        self.font_size = font_size
        self.x, self.y = x, y
        self.style = style
        self.rsp_file = 'wzife4.rsp'
        self.hash_id = 0xB5FDF1AC
        if self.style == CHAR_SPEECH:
            # 人物喊话
            self.rsp_file = 'wzife4.rsp'
            self.hash_id = 0x80E0B578
            self.default_color = '#W'
            self.x, self.y = 0, 0
        else:
            # 系统提示, 悬浮提示, 等
            self.default_color = '#Y'
        self.is_hover_enabled = True
        self.add_child('rich_text', RichText(width=PROMPT_WIDTH[self.style], font_size=self.font_size))
        self.rich_text.ori_x, self.rich_text.ori_y = PROMPT_MARGIN_X, PROMPT_MARGIN_Y

    @property
    def rich_text(self):
        return self.child('rich_text')

    def setup(self):
        super(GamePrompt, self).setup()  # 填充背景

        # 配置富文本
        self.rich_text.set_text(self.default_color + self.text)
        self.width = self.rich_text.actual_width + PROMPT_MARGIN_X * 2
        self.height = self.rich_text.max_height + PROMPT_MARGIN_Y * 2
        if self.style == CHAR_SPEECH:
            self.width = min(self.width, PROMPT_WIDTH[self.style] + PROMPT_MARGIN_X * 2)
            self.ori_x += (PROMPT_WIDTH[self.style] - self.width)//2
        elif self.style == FLOATING_PROMPT:
            self.width = self.width
        else:
            self.width = max(self.width, PROMPT_WIDTH[self.style])
        self.auto_sizing()

        # outline
        if self.style in [GAME_PROMPT, FLOATING_PROMPT]:
            self.setup_outline()

    def check_event(self):
        super(GamePrompt, self).check_event()
        if self.is_hover and self.director.match_mouse_event(STOP, MOUSE_RIGHT_DOWN):
            print('gp右键')
            self.remove_self()
            self.director.gp_manager.compose()


class SimplePrompt(GamePrompt):
    """
    简单提示
    """
    def __init__(self):
        super(SimplePrompt, self).__init__(style=FLOATING_PROMPT, font_size=16)
        self.add_child('rich_text', RichText(font_size=self.font_size, h_center=True))
        self.rich_text.ori_x, self.rich_text.ori_y = PROMPT_MARGIN_X, PROMPT_MARGIN_Y
        self.text = ''
        self.is_hover_enabled = False
        self.setup()

    def show(self, text):
        self.enable = True
        if text != self.text:
            self.text = text
            self.setup()

    def update(self):
        super(SimplePrompt, self).update()
        mpos = pygame.mouse.get_pos()
        self.x, self.y = mpos[0] - 20, mpos[1] - 20


class RichPrompt(ImageRect):
    def __init__(self):
        super(RichPrompt, self).__init__()
        self.width, self.height = 312, 172  # 默认提示大小
        self.icon_rsp = ''
        self.icon_hash = 0
        self.text_title = ''
        self.text = ''
        self.is_hover_enabled = False
        self.icon_margin = 0  # icon到左边缘和右边文字的距离
        fill_image_rect(self, 'wzife4.rsp', 0x80E0B578)
        icon = ImageRect()  # 大图标
        icon.is_hover_enabled = False
        icon.x, icon.y = 2, 10
        self.add_child('icon', icon)
        lb = Label(size=20, color=get_color('黄'), font_name=ADOBE_SONG, bold=True)  # 标题
        lb.x, lb.y = 123, 10
        lb.is_hover_enabled = False
        self.add_child('title', lb)
        rt = RichText(width=185, font_size=15)  # 文本
        rt.is_hover_enabled = False
        rt.x, rt.y = 123, 33
        self.add_child('text', rt)

    @property
    def title_label(self):
        return self.child('title')

    @property
    def rich_text(self):
        return self.child('text')

    @property
    def icon_image(self):
        return self.child('icon')

    def setup(self):
        # 先计算背景高度
        self.title_label.text = self.text_title
        self.title_label.setup()
        self.rich_text.set_text(self.text)
        total_height = 33 + self.rich_text.max_height
        self.height = max(172, total_height)

        # 图标
        fill_image_rect(self.icon_image, self.icon_rsp, self.icon_hash)

        # 如果是小尺寸图标
        if self.icon_image.width < 60:
            self.icon_margin = 20
            self.icon_image.ori_x = self.icon_margin
            self.rich_text.ori_x = self.icon_margin + self.icon_image.width + self.icon_margin
            self.title_label.ori_x = self.icon_margin + self.icon_image.width + self.icon_margin
            self.width = self.icon_margin + self.icon_image.width + self.icon_margin + 185 + 10

        self.auto_sizing(self.width, self.height)
        self.setup_outline()

    def show(self, icon_rsp, icon_hash, title, text:str):
        if not text.endswith('。'):
            text = text + '。'
        if icon_rsp != self.icon_rsp or icon_hash != self.icon_hash or title != self.text_title or text != self.text:
            self.icon_rsp, self.icon_hash, self.text_title, self.text = icon_rsp, icon_hash, title, text
            self.setup()
        self.enable = True

    def update(self):
        super().update()
        # 自动调整位置
        self.x, self.y = game.director.mouse_pos
        self.bottom_left_y = game.director.mouse_pos[1] - 10
        if self.top_left_y < 0:
            self.top_left_y = game.director.mouse_pos[1] + 30
        self.center_x = game.director.mouse_pos[0]
        if self.top_left_x < 0:
            self.top_left_x = 10
        if self.top_right_x > game.director.window_w:
            self.top_right_x = game.director.window_w - 10
