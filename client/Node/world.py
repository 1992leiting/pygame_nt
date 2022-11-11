import math
import os.path

import pygame

from Node.node import Node
import time
from Node.character import NPC, Character
from Node.portal import Portal
from Node.map_mask import MapMask
from Node.image_rect import ImageRect
from Node.animation import Animation8D
from Common.constants import *
from Common.common import *
from Node.camera import Camera
from Common.socket_id import *

from Game.res_manager import read_mapx, fill_res
# ca_mapx = read_mapx(1001)
# jy_mapx = read_mapx(1501)


class World(Node):
    def __init__(self):
        super(World, self).__init__()
        self.xy_timer = 0
        self.map_id = 0
        self.setup_ui()

    def setup_ui(self):
        self.add_child('map_jpg', Node())
        self.add_child('hero', Node())
        self.add_child('camera', Camera())

    def update_hero_xy(self):
        hero = game.hero
        send_data = {
            'x': hero.game_x,
            'y': hero.game_y,
            'mapid': self.map_id
        }
        self.director.client.send(C_更新坐标, send_data)

    def add_npc(self, data: dict):
        if 'msg' in data:
            data = data['msg']
        npc = NPC()
        npc.type = 'npc'
        npc.set_data(data)
        self.add_child('npc_' + str(npc.id), npc)
        # print('add npc:', npc.name)
        npc.visible = not self.director.IN_BATTLE

    def change_map(self, map_id):
        print('change map:', map_id)
        self.map_id = map_id
        map_file = map_dir + str(map_id) + '.mapx'
        if not os.path.exists(map_file):
            print('map不存在:', map_id)
            return
        self.remove_all_npcs()
        # self.remove_all_portals()
        # self.remove_all_players()
        # self.remove_all_masks()
        # self.remove_map_jpg()
        # if map_id == 1001:
        #     self.director.mapx = ca_mapx
        # elif map_id == 1501:
        #     self.director.mapx = jy_mapx
        # else:
        self.director.mapx = read_mapx(map_id)
        # 镜头(先移动镜头, 避免先加载资源之后跳转地图瞬间快速闪动)
        hero = game.hero
        camera = game.camera
        camera.limit = [0, 0, self.director.mapx.width - self.director.window_w, self.director.mapx.height - self.director.window_h]
        camera.move_to(hero.map_x, hero.map_y)
        # 底图
        map_jpg = ImageRect()
        self.director.astar.cell = self.director.mapx.navi
        map_jpg.image = self.director.mapx.jpg
        self.add_child('mapjpg', map_jpg)
        # 传送阵
        for pid, portal in portals.items():
            map_id = portal['原地图']
            if int(map_id) == self.director.mapx.map_id:
                p = Portal()
                p.portal_id = pid
                p.game_x, p.game_y = int(float(portal['原地图x'])), int(float(portal['原地图y']))
                self.add_child('portal_' + str(pid), p)
        # 遮罩
        for mask in self.director.mapx.masks:
            self.add_child('mapmask_' + str(mask.id), mask)

        self.change_state(self.director.is_in_battle)

    def remove_map_jpg(self):
        self.remove_child('mapjpg')

    def remove_all_npcs(self):
        for child_name, child in self.get_children().copy().items():
            if 'npc_' in child_name:
                self.remove_child(child_name)

    def remove_all_portals(self):
        for child_name, child in self.get_children().copy().items():
            if 'portal_' in child_name:
                self.remove_child(child_name)

    def remove_all_players(self):
        for child_name, child in self.get_children().copy().items():
            if type(child) == Character and child.type == 'player':
                self.remove_child(child_name)

    def remove_all_masks(self):
        for child_name, child in self.get_children().copy().items():
            if 'mapmask_' in child_name:
                self.remove_child(child_name)

    def change_state(self, state: bool):
        """
        切换状态
        :param state: True:战斗, False:非战斗
        :return:
        """
        print('world change state:', state)
        for name, child in self.get_children().copy().items():
            # 战斗时, portal/mapmask/npc隐藏, 反之显示
            if 'portal_' in name or 'mapmask_' in name or 'npc_' in name:
                self.child(name).visible = not state
        # 战斗时, hero隐藏, 反之显示
        self.child('hero').visible = not state
        # 战斗时, 关闭ysort
        self.ysort = not state

        # 若切换至非战斗, 删除战斗相关节点
        if not state:
            self.remove_child('grey_mask')
            self.remove_child('black_mask')
            self.remove_child('circle_mask')
            self.remove_child('units')

        if state:
            camera = game.camera
            # 纯色背景(战斗)
            node = ImageRect().from_color((15, 25, 60, 190))
            node.x, node.y = camera.x, camera.y
            self.add_child('grey_mask', node)
            # 黑色背景(战斗)
            node = ImageRect().from_color((0, 0, 0, 255))
            node.x, node.y = camera.x, camera.y
            node.visible = False
            self.add_child('black_mask', node)
            # 法阵圆圈(战斗)
            node = Animation8D()
            # fill_res(node, 'wzife.rsp', 0xD4BAB272)
            fill_res(node, 'addon.rsp', 0xE3B87E0F)
            # node.x, node.y = camera.x + 400, camera.y + 340
            node.x, node.y = 0, 200
            # node = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
            #                                      'hash_id': 0xDE3F48B7,
            #                                      'top_left_x': 300,
            #                                      'top_left_y': 400})
            self.add_child('circle_mask', node)
            # 战斗场景(战斗)
            from Battle.battle_scene import BattleScene
            bs = BattleScene()
            bs.x, bs.y = camera.x, camera.y
            self.add_child('battle_scene', bs)
        # 切换音乐
        if state:
            play_battle_music('战斗BOSS1')
        else:
            play_scene_bgm(self.map_id)

    def check_event(self):
        super(World, self).check_event()
        if self.director.match_mouse_event(STOP, MOUSE_LEFT_DOWN):
            hero = game.hero
            camera = game.camera
            if hero.visible:
                mouse_x, mouse_y = int(pygame.mouse.get_pos()[0] + camera.x), int(pygame.mouse.get_pos()[1] + camera.y)
                hero_x, hero_y = int(hero.map_x), int(hero.map_y)
                # print('鼠标点击:', (hero_x, hero_y), (mouse_x, mouse_y))
                path = self.director.astar.find_path((hero_x, hero_y), (mouse_x, mouse_y))
                hero.path = path
                # print('path:', path)

    def update(self):
        if self.director.is_in_battle:
            return
        # 更新主角坐标
        if time.time() - self.xy_timer > 1:
            self.update_hero_xy()
            self.xy_timer = time.time()
        # 距离主角一定范围内才显示
        hero = self.director.get_node('scene/world_scene/hero')
        for child_name in self.get_children().copy().keys():
            child = self.child(child_name)
            if type(child) == NPC or type(child) == Character or type(child) == MapMask:
                if child == game.hero:
                    break
                dis = math.dist((child.map_x, child.map_y), (hero.map_x, hero.map_y))
                if dis < 600:
                    child.visible = True
                if dis > 650:
                    child.visible = False