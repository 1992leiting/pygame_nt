from Node.node import Node
from Game.res_manager import fill_res
from Node.button import Button


class Scrollbar(Node):
    def __init__(self):
        super().__init__()
        self.width = 18
        self.height = 100
        btn = Button()
        fill_res(btn, 'wzife.rsp', 0xFD3D61F2)  # 上翻按钮,18*19
        self.add_child('scroll_up', btn)

        btn = Button()
        fill_res(btn, 'wzife.rsp', 0x09217E13)  # 下翻按钮,18*19
        self.add_child('scroll_down', btn)

        btn = Button()
        fill_res(btn, 'wzife4.rsp', 0x88E9B473)  # 滑动条
        self.add_child('scroll_bar', btn)

    def setup(self):
        pass