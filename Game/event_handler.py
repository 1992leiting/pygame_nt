import sys
import pygame.event

from Common.constants import *
from Common import common
import time


class EventHandler:
    def __init__(self, director):
        self.director = director

    def update(self):
        for event in pygame.event.get():
            self.check_quit_event(event)  # 窗口退出事件
            self.check_keyboard_event(event)  # 键盘按键
            self.check_mouse_event(event)  # 鼠标事件
            self.check_text_input_event(event)  # 文本输入事件(打字)

    def check_quit_event(self, event):
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
            # game_exit()
            # win = self.director.WD_EXIT
            # self.director.WINDOWLAYER.window_switch(win, True)
            pygame.quit()
            sys.exit()

    def check_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:  # 键盘按键按下
            key = event.key
            if key == pygame.K_RALT or key == pygame.K_LALT:
                self.director.alt_down = True

            elif key == pygame.K_RCTRL or key == pygame.K_LCTRL:
                self.director.ctrl_down = True

            else:
                # 测试
                if key == pygame.K_F1:
                    common.play_skill_effect_sound('地狱烈火')
                if key == pygame.K_F2:
                    common.play_skill_effect_sound('龙卷雨击')
                if key == pygame.K_F3:
                    common.play_char_sound('龙太子', '施法')
                if key == pygame.K_F4:
                    common.play_char_sound('龙太子', '倒地')
                if key == pygame.K_F5:
                    self.director.is_in_battle = True
                    self.director.child('world').change_state(True)
                if key == pygame.K_F6:
                    self.director.is_in_battle = False
                    self.director.child('world').change_state(False)
                if key == pygame.K_UP:
                    v = pygame.mixer.music.get_volume()
                    common.set_bgm_volume(v + 0.1)
                if key == pygame.K_DOWN:
                    v = pygame.mixer.music.get_volume()
                    common.set_bgm_volume(v - 0.1)
            self.director.kb_event = [event.type, key]

        if event.type == pygame.KEYUP:  # 键盘按键弹起
            key = event.key
            if key == pygame.K_RALT or key == pygame.K_LALT:
                self.director.alt_down = False

            elif key == pygame.K_RCTRL or key == pygame.K_LCTRL:
                self.director.ctrl_down = False
            self.director.kb_event = [event.type, key]

    def check_mouse_event(self, event):
        if self.director.mouse_event in [MOUSE_LEFT_RELEASE, MOUSE_RIGHT_RELEASE]:
            self.director.mouse_event = None

        if event.type == pygame.MOUSEWHEEL:  # 鼠标滚轮
            self.director.mouse_scroll_y = event.y  # 滚动的数量
        else:
            self.director.mouse_scroll_y = 0

        if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:  # 鼠标左键按下
                self.director.mouse_event = MOUSE_LEFT_DOWN
                self.director.mouse_left_down_time = time.time()
                self.director.is_mouse_left_released = True

            if mouse[2]:  # 鼠标右键按下
                self.director.mouse_event = MOUSE_RIGHT_DOWN
                self.director.is_mouse_right_released = True

        if event.type == pygame.MOUSEBUTTONUP:  # 鼠标弹起
            if event.button == 1:  # 鼠标左键弹起
                self.director.mouse_event = MOUSE_LEFT_RELEASE
                self.director.mouse_left_down_time = 9999999999
                self.director.is_mouse_left_released = False

            elif event.button == 3:  # 鼠标右键弹起
                self.director.mouse_event = MOUSE_RIGHT_RELEASE
                self.director.is_mouse_right_released = False

    def check_text_input_event(self, event):
        if event.type == pygame.TEXTINPUT:  # text输入
            # self.director.BASELAYER.speak_input.append_text(event.__dict__['text'])
            self.director.kb_text = event.__dict__['text']
