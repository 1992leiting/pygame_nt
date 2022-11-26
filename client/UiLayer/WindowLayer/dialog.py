from UiLayer.WindowLayer.window_layer import Window
from Common.constants import *
from Common.common import *
from Node.animation import Animation8D
from Node.label import Label
from Node.rich_text import RichText
from Node.node import Node
from Node.button import DialogOptionItem, ButtonClassicClose


class Dialog(Window):
    def __init__(self):
        super(Dialog, self).__init__()
        self.visible = False
        self.window_title = '对话栏'
        self.width, self.height = 550, 178
        self.x = self.director.window_w - self.width
        self.has_title_ui = False
        self.is_draggable = False
        self.char_model = '男人_巫医'
        self.char_name = '未知'
        self.text = '网易大神是网易游戏旗下的精英玩家社区。这里汇聚了广大精英玩家、游戏圈红人、行业大咖，集合了网易独家的官方资讯和福利趣闻，旨在为玩家打造一个丰富的游戏兴趣社交圈。玩家可以在网易大神与游戏中的好友实时聊天、多元互动；以游戏会友，结交更多游戏同好，和大神一起发现更多游戏乐趣。'
        self.options = ['我要干死三石!不是他死就是他亡!', '我只是来看看']
        self.setup()

    def show(self, model: str, name: str, text: str, options: list):
        self.char_model = model
        self.char_name = name
        self.text = text
        self.options = options
        self.setup()
        self.visible = True

    def setup(self):
        from Game.res_manager import fill_res
        super(Dialog, self).setup()
        # 大头像
        head = Animation8D()
        fill_res(head, head_image[self.char_model]['大头像文件'], head_image[self.char_model]['大头像'])
        head.x, head.y = 20, -head.height
        self.add_child('head_image', head)
        # 阴影
        shadow = Animation8D()
        fill_res(shadow, 'wzife4.rsp', 0x260BE57C)
        shadow.x, shadow.y = 0, -shadow.height
        self.add_child('shadow', shadow)
        # 名称
        name = Label(text=self.char_name, size=16)
        name.center_x, name.y = 90, -name.height - 6
        self.add_child('name', name)
        # 文本
        rich = RichText(text=self.text, width=515, font_size=15)
        rich.x, rich.y = 18, 18
        self.add_child('text', rich)

        # 选项
        self.add_child('option_area', Node())
        self.child('option_area').ori_x = 18
        self.child('option_area').y = self.child('text').y + self.child('text').max_height + 15
        self.child('option_area').clear_children()
        _y = 0
        for op in self.options:
            item = DialogOptionItem(op)
            item.y = _y
            self.child('option_area').add_child(item.uuid, item)
            _y += 26

        # 关闭
        close = ButtonClassicClose()
        self.add_child('close', close)
        close.ori_x = self.width - 23
        close.ori_y = 5

        self.center_x = self.director.window_w//2
        self.top_left_y = self.director.window_h//2

    def check_event(self):
        super(Dialog, self).check_event()
        if self.director.match_mouse_event(STOP, MOUSE_RIGHT_RELEASE):
            self.visible = False
