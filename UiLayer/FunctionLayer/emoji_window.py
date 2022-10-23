from Node.node import Node
from Node.image_rect import ImageRect
from Node.animation import Animation8D
from Node.emoji import Emoji
from Common.common import *
from Common.constants import *


class EmojiWindow(Node):
    def __init__(self):
        super(EmojiWindow, self).__init__()
        from Game.res_manager import fill_res
        self.width, self.height = 520, 400

        背景 = ImageRect()
        fill_res(背景, 'wzife4.rsp', 0x80E0B578)
        背景.image = auto_sizing(背景.image, self.width, self.height)
        背景.背景, 背景.height = self.width, self.height
        背景.bottom_left_x, 背景.bottom_left_y = self.director.window_w - 600, self.director.window_h - 35
        背景.setup_outline()
        self.add_child('背景', 背景)

        dx, dy = self.child('背景').top_left_x + 10, self.child('背景').top_left_y + 40
        line_height = 0  # 当前行的高度(取当前行最高表情的高度)
        # w = 0  # 上一个表情包的宽度
        for i, emoji_hash in enumerate(MY_EMOJI):
            emoji = Emoji()
            emoji.id = i
            fill_res(emoji, 'wzife.rsp', emoji_hash)
            line_height = max(line_height, emoji.height)
            emoji.x, emoji.y = dx, dy
            self.add_child(str(i), emoji)
            dx += emoji.width
            if dx + emoji.width >= self.width + self.child('背景').top_left_x:
                dx = self.child('背景').top_left_x + 10
                dy += line_height
                line_height = 0
            if i == 120:
                break

    # def draw(self):
    #     for child in self.get_children().copy().values():
    #         pygame.draw.rect(self.director.SCREEN, (255, 255, 255), child.rect, 2)
    #         pygame.draw.circle(self.director.SCREEN, (255, 0, 0), (child.x, child.y), 4)
