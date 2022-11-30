from UiLayer.WindowLayer.window_layer import Window
from Node.text_edit import LineEditWithBg
from Node.button import ButtonClassicRed
from Node.label import Label
from Common.socket_id import *
from Node.image_rect import ImageRect
from Common.constants import *
import pygame
from Game.res_manager import fill_res


class Smap(Window):
    def __init__(self):
        super(Smap, self).__init__()
        self.enable = False
        self.window_title = '小地图'
        self.width, self.height = 600, 400
        self.has_title_ui = False
        self.map_id = 0  # 当前窗口所记录的map_id
        self.setup()
        self.setup_win_config()
        self.add_child('smap_img', ImageRect())
        dot = ImageRect()
        fill_res(dot, 'wzife.rsp', 0x393947EB)
        self.add_child('hero_dot', dot)

    @property
    def smap_img(self):
        return self.child('smap_img')

    @property
    def scale_x(self):
        return game.director.mapx.width / self.smap_img.width

    @property
    def hover_x(self):
        mpos = pygame.mouse.get_pos()
        return int((mpos[0] - self.smap_img.x)*self.scale_x/20)

    @property
    def hover_y(self):
        mpos = pygame.mouse.get_pos()
        return int((mpos[1] - self.smap_img.y)*self.scale_y/20)

    @property
    def scale_y(self):
        return game.director.mapx.height / self.smap_img.height

    def setup_win_config(self, file=None, given_node=None):
        pass

    def switch(self, visible):
        super(Smap, self).switch(visible)
        if self.enable:
            if self.map_id != game.world.map_id:
                self.map_id = game.world.map_id
                # 加载小地图图片
                from Game.res_manager import fill_res
                smap_hash = int(BH_MAP_DATA[game.world.map_id]['小地图'])
                smap_img = ImageRect()
                smap_img.is_hover_enabled = True
                fill_res(smap_img, 'smap.rsp', smap_hash)
                self.add_child('smap_img', smap_img)
                # 调整背景大小
                self.width = smap_img.width + 30
                self.height = smap_img.height + 50
                self.setup()

                self.smap_img.center_x = self.center_x
                self.smap_img.center_y = self.center_y - 10

    def update(self):
        super(Smap, self).update()
        # 更新hero红点
        if self.child('hero_dot'):
            hx, hy = game.hero.map_x, game.hero.map_y
            dx = hx / self.scale_x
            dy = hy / self.scale_y
            self.child('hero_dot').ori_x = dx + 15
            self.child('hero_dot').ori_y = dy + 15

    def check_event(self):
        super(Smap, self).check_event()
        # 显示指向坐标
        if self.smap_img.is_hover:
            game.fp.show(' {}, {} '.format(self.hover_x, self.hover_y))
        if game.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
            xx = self.hover_x * 20
            yy = self.hover_y * 20
            print('小地图点击:', xx, yy)
            path = self.director.astar.find_path((game.hero.map_x, game.hero.map_y), (xx, yy))
            if path:
                self.director.client.send(C_发送路径, dict(路径=path))

