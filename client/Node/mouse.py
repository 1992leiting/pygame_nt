from Node.node import Node
from Node.animation import Animation8D
import pygame
from Node.image_rect import ImageRect


class Mouse(Node):
    def __init__(self):
        super(Mouse, self).__init__()
        self.res = {
            '攻击': ('wzife.rsp', 0x1FBC5273),
            '道具': ('wzife.rsp', 0xB48A9B3D),
            '捕捉': ('wzife.rsp', 0xC5750B15),
            '保护': ('wzife.rsp', 0xB352AE45),
            '禁止': ('wzife.rsp', 0x1733E33B),
            '输入': ('wzife.rsp', 0xC0247799),
            '事件': ('wzife4.rsp', 0xB3662702),
            '组队': ('wzife.rsp', 0x183DC759),
            '给予': ('wzife.rsp', 0xCF1D211E),
            '交易': ('wzife.rsp', 0xB87E0F0C),
            '平时攻击': ('wzife.rsp', 0x1FBC5273),
            '添加好友': ('wzife.rsp', 0x31A416A7),
            '指向': ('wzife.rsp', 0x5A055B13),
            '普通': ('general.rsp', 0x81DD40DC),
        }
        self.state = '普通'
        self.last_state = self.state

        img = ImageRect()
        self.add_child('grasp', img)  # 抓取对象的图标

        a8d = Animation8D()
        self.add_child('mouse_ani', a8d)
        self.setup()

    def setup(self):
        from Game.res_manager import fill_animation8d
        fill_animation8d(self.child('mouse_ani'), self.res[self.state][0], self.res[self.state][1])
        self.is_hover_enabled = False

    def set_last_state(self):
        self.change_state(self.last_state)

    def change_state(self, st):
        # print('change mouse:', st)
        if st != self.state and st in self.res.keys():
            self.last_state = self.state
            self.state = st
            self.setup()

    def clear_grasp_icon(self):
        img = ImageRect()
        self.add_child('grasp', img)  # 抓取对象的图标

    def update(self):
        self.child('mouse_ani').x, self.child('mouse_ani').y = pygame.mouse.get_pos()
        self.child('grasp').center_x, self.child('grasp').center_y = pygame.mouse.get_pos()
