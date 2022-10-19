from Node.animation import Animation8D
from common import *
from constants import *
from Node.node import Node
import time


class BuffEffect(Animation8D):
    """
    Buff/debuff特效, 要区分是否在主体上层(比如变身), 是否在主体头顶(比如红灯/蓝灯)
    """
    def __init__(self, name):
        super(BuffEffect, self).__init__()
        self.name = name
        self.is_in_front = True  # True:显示在主体上层 False:显示在主体下层
        self.is_on_top = False  # 是否在头顶
        self.setup()

    def setup(self):
        from res_manager import fill_magic_effect
        fill_magic_effect(self, '状态_' + self.name)
        front, on_top, offset = get_buff_effect_position(self.name)
        self.is_in_front = front
        self.is_on_top = on_top
        self.x += offset[0]
        self.y =+ offset[1]


class MagicEffect(Animation8D):
    """
    法术特效, 继承Animation8D, 封装了一些方法, 用于判断关键帧
    """
    def __init__(self, name):
        super(MagicEffect, self).__init__()
        self.attack_stage = 0  # 多个攻击帧时, 标记当前的攻击段, -1时表示攻击帧完成
        self.name = name  # 法术名称
        self.delay_time = 0
        self.setup()

    @property
    def attack_frame(self):
        return get_magic_attack_frame(self.name)[0]

    def setup(self):
        from res_manager import fill_magic_effect
        fill_magic_effect(self, self.name)
        if self.name == '反震':
            self.frame_index = 3

    def reach_attack_frame(self):
        """
        是否到达攻击帧, 到达时攻击段+=1, 没有下一段时置-1
        :return:
        """
        if self.attack_stage < len(self.attack_frame):
            if self.frame_index == self.frame_num + self.attack_frame[self.attack_stage] - 1:
                self.attack_stage += 1
                return True
            else:
                return False
        else:
            self.attack_stage = -1
            return False

    def reach_end_frame(self):
        """
        是否到达最后一帧
        :return:
        """
        if self.frame_index == self.frame_num - 1:
            return True
        else:
            return False


class FullScreenEffect(Node):
    """
    全屏法术特效
    """
    def __init__(self, name):
        super(FullScreenEffect, self).__init__()
        self.name = name  # 法术名称
        self.effects = {}  # 所有的特效动画
        self.black_bg = False  # 黑屏背景
        self.frame_index = 0
        self.attack_frame = [0]  # 攻击帧
        self.attack_stage = 0  # 攻击段
        self.fps_scale = 1
        self.index = 0
        self.time = 0  # 全屏动画开始的时间(加载完成的时间)
        self.is_ended = False  # 所有动画播放结束
        self.x, self.y = 280, 200
        self.setup()

    def add_child_effect(self, eff):
        self.add_child(str(self.index), eff)
        self.index += 1

    def reach_attack_frame(self):
        """
        是否到达攻击帧, 到达时攻击段+=1, 没有下一段时置-1
        :return:
        """
        if self.attack_stage < len(self.attack_frame):
            if self.frame_index == self.attack_frame[self.attack_stage] - 1:
                self.attack_stage += 1
                return True
            else:
                return False
        else:
            self.attack_stage = -1
            return False

    def setup(self):
        self.attack_stage = 0
        self.frame_index = 0
        # #################################
        if self.name == '龙卷雨击':
            self.black_bg = True
            self.attack_frame = [60, 70]
            self.fps_scale = 1.6

            eff = MagicEffect('龙卷雨击1')
            eff.x, eff.y = 60, 20
            eff.enable = False
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('龙卷雨击2')
            eff.x, eff.y = 110, 0
            eff.enable = False
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('龙卷雨击2')
            eff.x, eff.y = -120, 0
            eff.enable = False
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('龙卷雨击2')
            eff.x, eff.y = -80, 80
            eff.enable = False
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('龙卷雨击3')
            eff.x, eff.y = 0, 0
            eff.enable = False
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('龙卷雨击4')
            eff.x, eff.y = -100, 20
            eff.enable = False
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

        # #################################
        elif self.name == '落叶萧萧':
            self.black_bg = False
            self.attack_frame = [60, 70]
            self.fps_scale = 1

            eff = MagicEffect('落叶萧萧')
            eff.x, eff.y = 0, -30
            eff.enable = False
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('落叶萧萧2')
            eff.x, eff.y = 30, -30
            eff.enable = False
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('落叶萧萧2')
            eff.x, eff.y = -130, 0
            eff.enable = False
            eff.delay_time = 0.7
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('落叶萧萧2')
            eff.x, eff.y = -60, -70
            eff.enable = False
            eff.delay_time = 0.9
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('落叶萧萧2')
            eff.x, eff.y = 30, -40
            eff.enable = False
            eff.delay_time = 1.1
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('落叶萧萧2')
            eff.x, eff.y = -70, -90
            eff.enable = False
            eff.delay_time = 1.3
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('落叶萧萧2')
            eff.x, eff.y = -90, -90
            eff.enable = False
            eff.delay_time = 1.4
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

        # #################################
        elif self.name == '奔雷咒':
            self.black_bg = False
            self.attack_frame = [20, 60]
            self.fps_scale = 1.5

            eff = MagicEffect('奔雷咒2')
            eff.x, eff.y = -40, 0
            eff.enable = False
            eff.delay_time = 0
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('奔雷咒3')
            eff.x, eff.y = 40, 0
            eff.enable = False
            eff.delay_time = 0
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('奔雷咒')
            eff.x, eff.y = 0, 50
            eff.enable = False
            eff.delay_time = 0.2
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('奔雷咒')
            eff.x, eff.y = -100, 50
            eff.enable = False
            eff.delay_time = 0.5
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('奔雷咒')
            eff.x, eff.y = 80, 0
            eff.enable = False
            eff.delay_time = 0.8
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('奔雷咒2')
            eff.x, eff.y = -40, 0
            eff.enable = False
            eff.delay_time = 0.8
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('奔雷咒3')
            eff.x, eff.y = -40, 0
            eff.enable = False
            eff.delay_time = 0.5
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

        # #################################
        elif self.name == '地狱烈火':
            self.black_bg = False
            self.attack_frame = [50, 60]
            self.fps_scale = 1.8

            for i in range(1, 32):
                eff = MagicEffect('地狱烈火' + str(i))
                eff.set_fps(self.fps_scale * EFFECT_FPS)
                eff.enable = False
                if i == 1:
                    eff.x, eff.y = -300, 50 + 20
                    eff.delay_time = 0.1
                elif i == 2:
                    eff.x, eff.y = -300, -60 + 20
                    eff.delay_time = 0.1
                elif i == 3:
                    eff.x, eff.y = -300, -60 + 20
                    eff.delay_time = 0.2
                elif i == 4:
                    eff.x, eff.y = -300, 50 + 20
                    eff.delay_time = 0.2
                elif i == 5:
                    eff.x, eff.y = -300, 50 + 20
                    eff.delay_time = 0.3
                elif i == 6:
                    eff.x, eff.y = -300, 150 + 20
                    eff.delay_time = 0.3
                elif i == 7:
                    eff.x, eff.y = -300, 150 + 20
                    eff.delay_time = 0.6

                elif i == 8:
                    eff.x, eff.y = -150, -110 + 20
                    eff.delay_time = 0.4
                elif i == 9:
                    eff.x, eff.y = -150, -110 + 20
                    eff.delay_time = 0.5
                elif i == 10:
                    eff.x, eff.y = -150, 0 + 20
                    eff.delay_time = 0.5
                elif i == 11:
                    eff.x, eff.y = -150, 0 + 20
                    eff.delay_time = 0.6
                elif i == 12:
                    eff.x, eff.y = -150, 80 + 20
                    eff.delay_time = 0.6

                elif i == 13:
                    eff.x, eff.y = -150, 80 + 20
                    eff.delay_time = 0.7
                elif i == 14:
                    eff.x, eff.y = 0, -140 + 20
                    eff.delay_time = 0.7
                elif i == 15:
                    eff.x, eff.y = 0, -140 + 20
                    eff.delay_time = 0.8
                elif i == 16:
                    eff.x, eff.y = 0, -60 + 20
                    eff.delay_time = 0.8
                elif i == 17:
                    eff.x, eff.y = 0, -60 + 20
                    eff.delay_time = 0.9
                elif i == 18:
                    eff.x, eff.y = 0, 20 + 20
                    eff.delay_time = 0.9

                elif i == 19:
                    eff.x, eff.y = 0, 20 + 20
                    eff.delay_time = 1.0
                elif i == 20:
                    eff.x, eff.y = 150, -180 + 20
                    eff.delay_time = 1.0
                elif i == 21:
                    eff.x, eff.y = 150, -180 + 20
                    eff.delay_time = 1.1
                elif i == 22:
                    eff.x, eff.y = 150, -100 + 20
                    eff.delay_time = 1.1
                elif i == 23:
                    eff.x, eff.y = 150, -100 + 20
                    eff.delay_time = 1.2
                elif i == 24:
                    eff.x, eff.y = 150, -20 + 20
                    eff.delay_time = 1.2

                elif i == 25:
                    eff.x, eff.y = 150, -20 + 20
                    eff.delay_time = 1.3
                elif i == 26:
                    eff.x, eff.y = 300, -230 + 20
                    eff.delay_time = 1.3
                elif i == 27:
                    eff.x, eff.y = 300, -230 + 20
                    eff.delay_time = 1.4
                elif i == 28:
                    eff.x, eff.y = 300, -150 + 20
                    eff.delay_time = 1.4
                elif i == 29:
                    eff.x, eff.y = 300, -150 + 20
                    eff.delay_time = 1.5
                elif i == 30:
                    eff.x, eff.y = 300, -70 + 20
                    eff.delay_time = 1.5
                elif i == 31:
                    eff.x, eff.y = 300, -70 + 20
                    eff.delay_time = 1.5
                self.add_child_effect(eff)

        # #################################
        elif self.name == '水漫金山':
            self.black_bg = False
            self.attack_frame = [20, 60]
            self.fps_scale = 1.8

            eff = MagicEffect('水漫金山4')
            eff.x, eff.y = -110, -140
            eff.enable = False
            eff.delay_time = 0
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('水漫金山4')
            eff.x, eff.y = -150, -50
            eff.enable = False
            eff.delay_time = 0.2
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('水漫金山4')
            eff.x, eff.y = -150, 90
            eff.enable = False
            eff.delay_time = 0.4
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('水漫金山4')
            eff.x, eff.y = -30, 60
            eff.enable = False
            eff.delay_time = 0.5
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('水漫金山4')
            eff.x, eff.y = 70, -80
            eff.enable = False
            eff.delay_time = 0.6
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('水漫金山2')
            eff.x, eff.y = -30, 60
            eff.enable = False
            eff.delay_time = 0.5
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

        # #################################
        elif self.name == '泰山压顶':
            self.black_bg = False
            self.attack_frame = [16, 21]
            self.fps_scale = 1

            eff = MagicEffect('泰山压顶')
            eff.x, eff.y = 200, -100
            eff.enable = False
            eff.delay_time = 0
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

            eff = MagicEffect('泰山压顶2')
            eff.x, eff.y = -30, 40
            eff.enable = False
            eff.delay_time = 0.6
            eff.set_fps(self.fps_scale * EFFECT_FPS)
            self.add_child_effect(eff)

        self.time = time.time()

    def update(self):
        for child_name, child in self.get_children().items():
            if time.time() - self.time >= child.delay_time and not child.enable:
                child.enable = True
        for child_name, child in self.get_children().copy().items():
            if child.reach_end_frame():
                self.remove_child(child_name)
        if not self.get_children():
            self.is_ended = True
            self.visible = False

        self.frame_index += 1
