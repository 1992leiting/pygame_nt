from Node.node import Node
from Node.image_rect import ImageRect
from Node.rich_text import RichText
import time
from Common.constants import *


class PromptManager(ImageRect):
    """
    弹出管理器,计算位置,超时消失,等
    """
    def __init__(self, style=GAME_PROMPT, x=300, y=300):
        super(PromptManager, self).__init__()
        self.x, self.y = x, y
        self.is_hover_enabled = True
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

        # for _, child in self.get_children().items():
        #     child.setup_outline()

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
    def __init__(self, txt='默认提示...', style=GAME_PROMPT, x=0, y=0):
        super(GamePrompt, self).__init__()
        print('prompt item:', txt)
        self.time = time.time()
        self.text = txt
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
            # 系统提示, 等
            self.default_color = '#Y'
        self.is_hover_enabled = True

        self.rich_text = RichText(width=PROMPT_WIDTH[self.style])
        self.rich_text.ori_x, self.rich_text.ori_y = PROMPT_MARGIN_X, PROMPT_MARGIN_Y
        self.add_child('rich_text', self.rich_text)

    def setup(self):
        super(GamePrompt, self).setup()  # 填充背景

        # 配置富文本
        self.rich_text.set_text(self.default_color + self.text)
        self.width = self.rich_text.actual_width + PROMPT_MARGIN_X * 2
        self.height = self.rich_text.max_height + PROMPT_MARGIN_Y * 2
        if self.style == CHAR_SPEECH:
            self.width = min(self.width, PROMPT_WIDTH[self.style] + PROMPT_MARGIN_X * 2)
            self.ori_x += (PROMPT_WIDTH[self.style] - self.width)//2
        else:
            self.width = max(self.width, PROMPT_WIDTH[self.style])
        self.auto_sizing()
        # self.setup_outline((255, 255, 255))  # 添加outline

    def check_event(self):
        super(GamePrompt, self).check_event()
        if self.is_hover and self.director.match_mouse_event(STOP, MOUSE_RIGHT_DOWN):
            print('gp右键')
            self.remove_self()
            self.director.gp_manager.compose()
