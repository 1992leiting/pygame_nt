from Node.node import Node
from Node.image_rect import ImageRect
from Node.rich_text import RichText
import time
from Common.constants import *

GP_START_X = 300  # 系统提示的初始坐标
GP_START_Y = 300
GP_MARGIN_X = 5  # 系统提示文字距离边框的距离
GP_MARGIN_Y = 5
GP_SPACE = 5  # 系统提示之间的间距


class GamePromptManager(ImageRect):
    def __init__(self):
        super(GamePromptManager, self).__init__()
        self.next_x, self.next_y = 300, 300  # 下一条提示的坐标
        self.is_hover_enabled = True
        self.is_draggable = False
        self.rsp_file = 'wzife.rsp'
        self.hash_id = 0x4CFB6A98
        self.setup()
        self.x, self.y = GP_START_X - self.width - 2, GP_START_Y - self.height - 2

    def append(self, text):
        print('添加提示:', text)
        new_pt = GamePrompt(text)
        new_pt.setup()
        self.add_child(new_pt.uuid, new_pt)
        self.compose()

    def compose(self):
        pt_list = list(self.get_children().copy().values())
        pt_list.reverse()
        _x, _y = GP_START_X, GP_START_Y
        for i in range(0, len(pt_list)):
            pt = pt_list[i]
            # _x = GP_START_X
            _y = _y - GP_SPACE - pt.height
            pt.x, pt.y = _x, _y
        for _, child in self.get_children().items():
            child.setup_outline()

    def check_event(self):
        super(GamePromptManager, self).check_event()
        self.visible = self._children

    def update(self):
        super(GamePromptManager, self).update()
        # 删除过期提示
        for name, child in self.get_children().copy().items():
            if time.time() - child.time > 5:
                self.remove_child(name)
                self.compose()


class GamePrompt(ImageRect):
    """
    系统提示
    """
    def __init__(self, txt='默认提示...', x=300, y=300):
        super(GamePrompt, self).__init__()
        self.time = time.time()
        self.text = txt
        self.x, self.y = x, y
        self.rsp_file = 'wzife4.rsp'
        self.hash_id = 0xB5FDF1AC
        self.is_hover_enabled = True

        self.rich_text = RichText(width=300)
        self.rich_text.ori_x, self.rich_text.ori_y = GP_MARGIN_X, GP_MARGIN_Y
        self.add_child('rich_text', self.rich_text)

    def setup(self):
        super(GamePrompt, self).setup()  # 填充背景

        # 配置富文本
        self.rich_text.set_text('#Y' + self.text)
        self.width = self.rich_text.width + GP_MARGIN_X * 2
        self.height = self.rich_text.max_height + GP_MARGIN_Y * 2
        self.width = max(self.width, 300)
        self.auto_sizing()
        self.setup_outline((255, 255, 255))  # 添加outline

    def check_event(self):
        super(GamePrompt, self).check_event()
        if self.is_hover and self.director.match_mouse_event(STOP, MOUSE_RIGHT_DOWN):
            print('gp右键')
            self.remove_self()
            self.director.gp_manager.compose()
