from UiLayer.WindowLayer.window_layer import Window
from Node.text_edit import LineEditWithBg
from Node.button import ButtonClassicRed
from Node.label import Label
from Common.socket_id import *
from Node.image_rect import ImageRect
from Common.constants import *
import pygame
from Game.res_manager import fill_res
from Node.button import LabelButton, ClassicCheckButton
from Common.common import *
from Node.character import NPC


SMAP_IMG_SHIFT = 15


class NpcButton(LabelButton):
    def __init__(self, txt, size=14, color=(255, 255, 255)):
        super(NpcButton, self).__init__(txt, size, color)
        self.npc = None
        self.callback_func = None

    def check_event(self):
        super(NpcButton, self).check_event()
        if self.event:
            if self.callback_func:
                self.callback_func(self.npc)


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
        self.add_child('smap_img', ImageRect(with_mask=True))
        self.smap_img.is_hover_enable = True
        self.is_npc_visible = True
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
                # 切换地图后加载内容
                self.map_id = game.world.map_id
                # 加载小地图图片
                from Game.res_manager import fill_res
                smap_hash = int(BH_MAP_DATA[game.world.map_id]['小地图'])
                smap_img = ImageRect(with_mask=True)
                smap_img.is_hover_enabled = True
                fill_res(smap_img, 'smap.rsp', smap_hash)
                self.add_child('smap_img', smap_img)
                # 调整背景大小
                self.width = smap_img.width + SMAP_IMG_SHIFT * 2 + SMAP_IMG_SHIFT * 2 + 40
                self.height = max(smap_img.height + SMAP_IMG_SHIFT * 2, 270)
                self.setup()
                # 调整smap_img位置
                self.smap_img.ori_x = SMAP_IMG_SHIFT
                self.smap_img.ori_y = SMAP_IMG_SHIFT
                # 勾选框
                tps = ['全部', '普通', '商业', '特殊', '传送', '任务', '出口']
                _y = 20
                for tp in tps:
                    cb = ClassicCheckButton(tp, get_color(SMAP_NPC_COLOR[tp]))
                    cb.x, cb.y = self.smap_img.width + SMAP_IMG_SHIFT * 2, _y
                    self.add_child(tp, cb)
                    _y += 35
                # 加载小地图NPC名称
                self.smap_img.set_modulation((50, 50, 50, 50))
                for npc in game.world.cur_npcs:
                    name = npc.name
                    tp = npc.npc_type
                    # print(tp)
                    if tp in SMAP_NPC_COLOR:
                        color = get_color(SMAP_NPC_COLOR[tp])
                    else:
                        color = get_color('白')
                    btn = NpcButton(name, size=12, color=color)
                    btn.npc = npc
                    btn.callback_func = self.path_to_npc
                    btn.x, btn.y = npc.map_x/self.scale_x, npc.map_y/self.scale_y
                    self.smap_img.add_child('npc_'+str(npc.id), btn)

    def update(self):
        super(Smap, self).update()
        # 更新hero红点
        if self.child('hero_dot'):
            hx, hy = game.hero.map_x, game.hero.map_y
            dx = hx / self.scale_x
            dy = hy / self.scale_y
            self.child('hero_dot').ori_x = dx + SMAP_IMG_SHIFT
            self.child('hero_dot').ori_y = dy + SMAP_IMG_SHIFT
        # 显示指向坐标
        if self.is_active and self.smap_img.rect.collidepoint(pygame.mouse.get_pos()):
            game.fp.show(' {}, {} '.format(self.hover_x, self.hover_y))

    def check_event(self):
        super(Smap, self).check_event()
        if game.director.match_mouse_event(STOP, MOUSE_LEFT_RELEASE):
            xx = self.hover_x * 20
            yy = self.hover_y * 20
            path = self.director.astar.find_path((game.hero.map_x, game.hero.map_y), (xx, yy))
            if path:
                self.director.client.send(C_发送路径, dict(路径=path))

    def path_to_npc(self, npc: NPC):
        print('path to npc:', npc.name)
        nx, ny = npc.map_x, npc.map_y
        path = self.director.astar.find_path((game.hero.map_x, game.hero.map_y), (nx, ny))
        if path:
            self.director.client.send(C_发送路径, dict(路径=path))

