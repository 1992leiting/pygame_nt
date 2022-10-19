import time
from Node.node import Node
import pygame


class Animation(Node):
    def __init__(self):
        super().__init__()
        self.duration = 0.12  # 刷新间隔,秒
        self.fps = 10  # 每秒钟刷新的帧数
        self.fps_cnt = 0
        self.timer = 0
        self.kx, self.ky = 0, 0
        self.width, self.height = 0, 0
        self.frame_num = 0  # 总帧数
        self.frames = []  # 帧队列,元素为surface或者image
        self.frame_index = 0  # 帧序号
        self.cur_frame = None  # 当前的帧, Image类型
        self.highlight = False
        self.is_playing = True  # 动画是否播放

    def update(self):
        if self.is_playing:
            # 利用pygame FPS
            if self.fps_cnt >= int(self.director.GAME_FPS / self.fps):
                self.fps_cnt = 0
                self.frame_index = (self.frame_index + 1) % self.frame_num
            else:
                self.fps_cnt += 1

            # 利用时间间隔(不准确, 不同步)
            # if time.time() - self.timer > self.duration:
            #     self.timer = time.time()
            #     self.frame_index = (self.frame_index + 1) % self.frame_num

        self.cur_frame = self.frames[self.frame_index]

    def draw(self):
        if self.cur_frame:
            _frame = self.cur_frame.copy()
            if self.highlight:
                _frame.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_ADD)
            self.director.SCREEN.blit(_frame, (self.x - self.kx, self.y - self.ky))


class Animation8D(Node):
    """
    child为Animation类
    """
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.cur_animation = None
        self.is_playing = True

    @property
    def rect(self):
        if self.cur_animation:
            return self.cur_animation.rect
        else:
            return pygame.rect.Rect(0, 0, 0, 0)

    @property
    def frame_num(self):
        if self.cur_animation:
            return self.cur_animation.frame_num
        return 0

    def set_fps(self, d: int):
        for child in self.get_children().values():
            child.fps = d

    @property
    def frame_index(self):
        if self.cur_animation:
            return self.cur_animation.frame_index
        else:
            return 0

    @frame_index.setter
    def frame_index(self, idx):
        if self.cur_animation:
            self.cur_animation.frame_index = idx

    def update(self):
        for child in self.get_children().values():
            if self.direction >= self.get_children_count():
                self.direction -= 4
            if child.node_name == str(self.direction):
                self.cur_animation = child
                self.cur_animation.is_playing = self.is_playing
                self.width = self.cur_animation.width
                self.height = self.cur_animation.height
                child.visible = True
            else:
                child.visible = False
