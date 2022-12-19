from Node.node import Node
from Common.constants import *
from Node.animation import Animation8D


# offset = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
offset = [-5, -5, -5, -5, 5, 5, 5, 5]


class HpEffect(Node):
    """
    加血/掉血特效, 字符跳动效果
    """
    def __init__(self, value: int, hp_type=DAMAGE):
        super(HpEffect, self).__init__()
        self.value = value
        self.hp_type = hp_type
        self.ori_y = 0
        self.i = 0
        self.setup()

    def setup(self):
        from Game.res_manager import fill_res
        digits = str(self.value)
        for i, digit in enumerate(digits):
            dg = Animation8D()
            if self.hp_type == DAMAGE:
                fill_res(dg, 'misc.rsp', 0x30F737D8)
            elif self.hp_type == RECOVER:
                fill_res(dg, 'misc.rsp', 0x3CF8F9FE)
            dg.is_playing = False
            dg.frame_index = int(digit)
            dg.update()
            dg.x = 13 * i
            self.add_child(str(i), dg)
        # 根据数字位数移动坐标使居中
        dx = (len(digits) - 1) * 10 - 6
        for child in self.get_children().values():
            child.x -= dx
        self.ori_y = self.y

    @staticmethod
    def get_offset(i):
        if i >= len(offset) or i < 0:
            return 0
        else:
            return offset[i]

    def draw(self):
        # 字符跳动特效
        for k, child in enumerate(self.get_children().values()):
            child.y += self.get_offset(self.i - k * 2)
            if self.i - k * 2 >= len(offset) + 25:
                # self.remove_self()
                self.visible = False
                return

        self.i += 1
