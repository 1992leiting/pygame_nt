import random
import time

import pygame.mouse
from Common.common import *
from Node.animation import Animation8D
from Node.image_rect import ImageRect
from Common.constants import *
from Node.label import Label
from Node.magic_effect import MagicEffect, BuffEffect
from Node.node import Node
from Node.prompt import GamePrompt, PromptManager
from Common.socket_id import *


class BasicCharacter(Node):
    """
    基础人物类, 只有模型, 不显示名称
    """
    def __init__(self):
        super(BasicCharacter, self).__init__()
        self.shapes = shapes  # shapes:普通模型, bshapes:战斗模型
        self.model = "龙太子"
        self.weapon = ""
        self.name = '小菜菜'
        self.title = '江湖小虾'
        self.suit = ''
        self.is_moving = False
        self.clear_path = False
        self.path = []
        self.direction = 0
        self.id = 0
        self.type = 'char'
        self.color_recipe = (0, 0, 0)  # 分别代表3个部位不同的染色方案
        self.cur_char_animation = None
        self.cur_weapon_animation = None
        self.mask_rect = pygame.Rect(0, 0, 0, 0)
        self.mouse_filter = STOP
        self.setup_ui()

    @property
    def speed(self):
        return MOVING_SPEED * (60 // self.director.game_fps)  # 保证速度不会因为fps变化而变化

    def check_hover(self):
        pos = pygame.mouse.get_pos()
        rect_pos = (pos[0] - self.mask_rect.x, pos[1] - self.mask_rect.y)
        if self.director.node_hover == self:
            self.director.node_hover = None
        if self.director.node_hover is None and self.mask_rect.collidepoint(pos):
            if self.cur_char_animation:
                color = self.cur_char_animation.cur_frame.get_at(rect_pos)
                if color != (0, 0, 0, 0):
                    self.is_hover = True
                    self.director.node_hover = self
                else:
                    self.is_hover = False
            else:
                self.is_hover = False
        else:
            self.is_hover = False

    def setup_ui(self):
        # UI层
        self.add_child('front_buff', Node())  # 后置buff
        self.add_child('char_stand', Animation8D())  # 身体动画
        self.add_child('char_walk', Animation8D())  # 身体动画
        self.add_child('weapon_stand', Animation8D())  # 武器动画
        self.add_child('weapon_walk', Animation8D())  # 武器动画
        self.add_child('shadow', Node())  # 脚底阴影
        self.add_child('title', Node())  # 称谓
        self.add_child('name', Node())  # 名称
        self.add_child('front_buff', Node())  # 前置buff
        self.add_child('effect', Node())  # 特效(攻击特效,升级特效等)
        self.add_child('speech_prompt', PromptManager(style=CHAR_SPEECH))

    def set_data(self, data):
        if '模型' in data:
            self.model = data['模型']
        if '武器数据' in data:
            self.weapon = data['武器数据']['名称']
        if '武器' in data:
            self.weapon = data['武器']
        if '名称' in data:
            self.name = data['名称']
        if '称谓' in data:
            self.title = data['称谓']
        if '当前称谓' in data:
            self.title = data['当前称谓']
        if '地图数据' in data:
            self.game_x = int(data['地图数据']['x'])
            self.game_y = int(data['地图数据']['y'])
        if 'x' in data:
            if type(data['x']) == str:
                if '.' in data['x']:
                    data['x'] = data['x'].split('.')[0]
            self.game_x = int(data['x'])
        if 'y' in data:
            if type(data['y']) == str:
                if '.' in data['y']:
                    data['y'] = data['y'].split('.')[0]
            self.game_y = int(data['y'])
        if 'X' in data:
            if type(data['X']) == str:
                if '.' in data['X']:
                    data['X'] = data['X'].split('.')[0]
            self.game_x = int(data['X'])
        if 'Y' in data:
            if type(data['Y']) == str:
                if '.' in data['Y']:
                    data['Y'] = data['Y'].split('.')[0]
            self.game_y = int(data['Y'])
        if 'mx' in data:
            # if '.' in data['mx']:
            #     data['mx'] = data['mx'].split('.')[0]
            self.game_x = int(data['mx'])
        if 'my' in data:
            # if '.' in data['my']:
            #     data['my'] = data['my'].split('.')[0]
            self.game_y = int(data['my'])
        if '方向' in data:
            self.direction = int(data['方向'])
        if 'id' in data:
            self.id = int(data['id'])
        if '染色' in data:
            self.color_recipe = data['染色']
        # if '类型' in data:
        #     self.type = data['类型']
        self.setup()

    def setup(self):
        print('setup char:', self.name)
        self.setup_basic()

    def set_fps(self, v):
        for child_name, child in self.get_children().items():
            chd = self.child(child_name)
            if type(chd) == Animation8D:
                chd.set_fps(v)

    def set_path(self, p: list):
        """
        设置人物路径
        """
        self.path = p
        if p:
            pass
            # self.x, self.y = p[0]  # 直接移动到第一个路径坐标
        else:
            self.is_moving = False

    def setup_basic(self):
        if self.name == '大鹌鹑二号' or '风' in self.name:
            self.color_recipe = (4, 4, 0)
        from Game.res_manager import fill_animation8d, fill_image_rect
        self.setup_ui()
        model_index = self.model
        weapon_index = ""
        if self.weapon and self.weapon != "":
            weapon_index = self.weapon + "_" + self.model

        self.setup_ui()
        ani_char = Animation8D()
        # fill_animation8d(ani_char, self.shapes[model_index]['资源'], int(self.shapes[model_index]['静立']))
        _rsp, _hash = get_normal_shape_res_hash(model_index, '静立', self.shapes)
        fill_animation8d(ani_char, _rsp, _hash)
        ani_char.set_fps(7)
        self.add_child('char_stand', ani_char)

        self.width = self.child('char_stand').width
        self.height = self.child('char_stand').height

        if weapon_index and weapon_index != '':
            ani_weapon = Animation8D()
            # fill_animation8d(ani_weapon, self.shapes[weapon_index]['资源'], int(self.shapes[weapon_index]['静立']))
            _rsp, _hash = get_normal_shape_res_hash(weapon_index, '静立', self.shapes)
            fill_animation8d(ani_weapon, _rsp, _hash)
            ani_weapon.set_fps(7)
            self.add_child('weapon_stand', ani_weapon)

        ani_char = Animation8D()
        # fill_animation8d(ani_char, self.shapes[model_index]['资源'], int(self.shapes[model_index]['行走']))
        _rsp, _hash = get_normal_shape_res_hash(model_index, '行走', self.shapes)
        fill_animation8d(ani_char, _rsp, _hash)
        ani_char.set_fps(18)
        self.add_child('char_walk', ani_char)

        if weapon_index and weapon_index != '':
            ani_weapon = Animation8D()
            # fill_animation8d(ani_weapon, self.shapes[weapon_index]['资源'], int(self.shapes[weapon_index]['行走']))
            _rsp, _hash = get_normal_shape_res_hash(weapon_index, '行走', self.shapes)
            fill_animation8d(ani_weapon, _rsp, _hash)
            ani_weapon.set_fps(18)
            self.add_child('weapon_walk', ani_weapon)

        shadow = ImageRect()
        fill_image_rect(shadow, 'shape.rsp', 3705976162)
        self.add_child('shadow', shadow)

    def move(self):
        target = self.path[0]
        self.direction = calc_direction((self.ori_x, self.ori_y), target)
        vector = pygame.Vector2()
        vector.x, vector.y = int(target[0]) - self.ori_x, int(target[1]) - self.ori_y
        if vector.length() == 0:
            return
        vector.normalize_ip()
        vector.scale_to_length(self.speed)
        self.ori_x += vector.x
        self.ori_y += vector.y

    def update(self):
        self.update_path()
        self.update_basic()

    def update_path(self):
        if len(self.path) > 0:
            if self.clear_path:
                self.path = []
                self.clear_path = False
                self.is_moving = False
            else:
                self.is_moving = True
                _target = self.path[0]
                th = self.speed // 2 + 1
                if abs(self.ori_x - int(_target[0])) <= th and abs(self.ori_y - int(_target[1])) <= th:
                    self.path.pop(0)
                else:
                    self.move()
        else:
            self.is_moving = False

    def update_basic(self):
        if self.is_moving:
            if self.child('char_stand'):
                self.child('char_stand').enable = False
            if self.child('weapon_stand'):
                self.child('weapon_stand').enable = False
            if self.child('char_walk'):
                self.child('char_walk').enable = True
                self.cur_char_animation = self.child('char_walk').cur_animation
            if self.child('weapon_walk'):
                self.child('weapon_walk').enable = True
                self.cur_weapon_animation = self.child('weapon_walk').cur_animation
        else:
            if self.child('char_stand'):
                self.child('char_stand').enable = True
                self.cur_char_animation = self.child('char_stand').cur_animation
            if self.child('weapon_stand'):
                self.child('weapon_stand').enable = True
                self.cur_weapon_animation = self.child('weapon_stand').cur_animation
            if self.child('char_walk'):
                self.child('char_walk').enable = False
            if self.child('weapon_walk'):
                self.child('weapon_walk').enable = False

        # 染色
        if self.color_recipe != (0, 0, 0) and not self.cur_char_animation.is_modulated:
            from Game.res_manager import modulate_animation_by_palette
            wpal_file = '{}{}.wpal'.format(wpal_dir, self.model)
            if os.path.exists(wpal_file):
                if self.is_moving:
                    pal16 = self.child('char_walk').palette16
                else:
                    pal16 = self.child('char_stand').palette16
                modulate_animation_by_palette(self.cur_char_animation, wpal_file, pal16, self.color_recipe)
            else:
                print('染色文件不存在:', wpal_file)

        if self.child('char_stand'):
            self.child('char_stand').direction = self.direction
        if self.child('weapon_stand'):
            self.child('weapon_stand').direction = self.direction
        if self.child('char_walk'):
            self.child('char_walk').direction = self.direction
        if self.child('weapon_walk'):
            self.child('weapon_walk').direction = self.direction

        # MaskRect
        if self.cur_char_animation and self.cur_char_animation.cur_frame:
            mask = pygame.mask.from_surface(self.cur_char_animation.cur_frame)
            self.mask_rect = mask.get_rect()
            self.mask_rect.x = self.x - self.cur_char_animation.kx
            self.mask_rect.y = self.y - self.cur_char_animation.ky

        if self.cur_char_animation:
            self.cur_char_animation.highlight = self.is_hover
        if self.cur_weapon_animation:
            self.cur_weapon_animation.highlight = self.is_hover

        # 鼠标指向时指针变化
        if self.is_hover:
            if self.director.char_hover != self.id:
                self.director.char_hover = self.id
                if self.type == 'npc':
                    self.director.child('mouse').change_state('事件')
        else:
            if self.director.char_hover == self.id:
                self.director.char_hover = None
                if self.type == 'npc':
                    self.director.child('mouse').set_last_state()

        # 发言框
        self.child('speech_prompt').x = self.x - self.width//2 - (CHAR_SPEECH_PROMPT_WIDTH - self.width)//2
        self.child('speech_prompt').y = self.y - self.height + 10

    def check_event(self):
        # super(BasicCharacter, self).check_event()
        if self.is_hover:
            # 左键按下事件要吸收掉
            if self.director.match_mouse_event(self.mouse_filter, MOUSE_LEFT_DOWN):
                pass
            # 左键弹起则触发点击事件
            if self.director.match_mouse_event(self.mouse_filter, MOUSE_LEFT_RELEASE):
                # print('点击人物:', self.name, self.id)
                if self.type == 'npc':
                    send(C_点击NPC, dict(id=self.id))
                if self.type == 'player' and game.mouse.state == '攻击':
                    send_data = dict(target_pid=self.id, map_id=game.world.map_id, x=self.game_x, y=self.game_y)
                    send(C_攻击玩家, send_data)


class Character(BasicCharacter):
    def __init__(self):
        super(Character, self).__init__()
        self.type = 'player'

    def setup_character(self):
        name = Label()
        name.text = self.name
        name.font_name = 'mod_AdobeSong.ttf'
        name.size = 16
        name.color = (0, 255, 0)
        name.shadow = True
        name.setup()
        self.add_child('name', name)

        if self.title != '':
            title = Label()
            title.text = self.title
            title.font_name = 'mod_AdobeSong.ttf'
            title.size = 16
            title.color = (124, 255, 255)
            title.shadow = True
            title.setup()
            self.add_child('title', title)

    def setup(self):
        self.setup_basic()
        self.setup_character()

    def update_character(self):
        if self.title:
            self.child('title').center_x = self.x
            self.child('title').center_y = self.y + 20
            if self.child('name'):
                self.child('name').center_x = self.x
                self.child('name').center_y = self.y + 40
        else:
            if self.child('name'):
                self.child('name').center_x = self.x
                self.child('name').center_y = self.y + 20

    def update(self):
        self.update_path()
        self.update_basic()
        self.update_character()

        # if self.cur_char_animation:
        #     pygame.draw.rect(self.director.screen, (255, 255, 255), self.cur_char_animation.rect, 2)


class Hero(Character):
    def __init__(self):
        super(Hero, self).__init__()
        self.type = 'hero'

    def set_path(self, p: list):
        super(Hero, self).set_path(p)
        # from Game.res_manager import fill_res
        # points_canvas = game.world.child('map_jpg').child('hero_path_points')
        # points_canvas.clear_children()
        # for i, (x, y) in enumerate(p):
        #     point = ImageRect()
        #     fill_res(point, 'wzife.rsp', 0x18E4B31B)
        #     point.x, point.y = x, y
        #     points_canvas.add_child(str(i), point)

    # def update(self):
    #     super(Hero, self).update()
    #     # 寻路结束时清除寻路标记点
    #     if not self.path and game.world.child('map_jpg'):
    #         points_canvas = game.world.child('map_jpg').child('hero_path_points')
    #         points_canvas.clear_children()


class NPC(BasicCharacter):
    def __init__(self):
        super(NPC, self).__init__()
        self.type = 'npc'
        self.npc_type = '普通'
        self.shapes = shapes

    def setup_npc(self):
        name = Label()
        name.text = self.name
        name.font_name = 'mod_AdobeSong.ttf'
        name.size = 16
        name.color = (255, 255, 0)
        name.shadow = True
        name.setup()
        self.add_child('name', name)

        if self.title != '':
            title = Label()
            title.text = self.title
            title.font_name = 'mod_AdobeSong.ttf'
            title.size = 16
            title.color = (124, 255, 255)
            title.shadow = True
            title.setup()
            self.add_child('title', title)

    def setup(self):
        self.setup_basic()
        self.setup_npc()

    def set_data(self, data):
        super(NPC, self).set_data(data)
        if '事件' in data:
            self.npc_type = data['事件']
        if '类型' in data:
            self.npc_type = data['类型']

    def update_npc(self):
        if self.title:
            self.child('title').center_x = self.x
            self.child('title').center_y = self.y + 20
            if self.child('name'):
                self.child('name').center_x = self.x
                self.child('name').center_y = self.y + 40
        else:
            if self.child('name'):
                self.child('name').center_x = self.x
                self.child('name').center_y = self.y + 20

    def update(self):
        self.update_path()
        self.update_basic()
        self.update_npc()


class BattleUnit(BasicCharacter):
    def __init__(self):
        super(BattleUnit, self).__init__()
        self.bu_index = 0  # 战斗单位编号
        self.ori_x, self.ori_y = 0, 0  # 单位的原始站位坐标
        self.tmp_x, self.tmp_y = 0, 0  # 临时坐标
        self.shapes = bshapes
        self.h_speed = MOVING_SPEED * (60 // self.director.game_fps) * 15  # 保证速度不会因为fps变化而变化
        self.l_speed = self.h_speed / 10  # 高速/低速, 用于不同动作
        self.moving_speed = self.h_speed
        self.cur_action = '待战'
        self.is_ani_playing = True  # 动画是否在播放
        self.is_shaking = False  # 抖动
        self.camp = OUR  # 阵营(我方/敌方)
        self.is_moving_backward = 0  # 是否在击退状态
        self.backward_frame_cnt = 0  # 击退时的帧数计数器(用于计算动作保持时间)
        self.backward_fade_in = False  # 击退时的慢放效果
        self.is_moving_back = False  # 是否在归位状态
        self.attack_stage = 0  # 多段攻击时, 标记当前的攻击段, -1时表示攻击完成
        self.backward_acc_cnt = 0  # 累计后退的次数(多段攻击且每次都退后)
        self.attack_acc = False  # 多段击退是否累加后退距离
        self.is_dead = False  # 是否死亡状态
        self.setup_ui()

    def setup_ui(self):
        # UI层
        self.add_child('behind_buff', Node())  # 后置buff
        self.add_child('hp_bar', Node())  # 血条
        self.add_child('char', Node())  # 身体动画
        self.add_child('weapon', Node())  # 武器动画
        self.add_child('shadow', Node())  # 脚底阴影
        self.add_child('name', Node())  # 名称
        self.add_child('front_buff', Node())  # 前置buff
        self.add_child('effect', Node())  # 特效(攻击特效,升级特效等)

    @property
    def frame_num(self):
        """
        动画总帧数, 取人物动画帧数
        :return:
        """
        if self.child('char'):
            return self.child('char').frame_num
        return 0

    @property
    def frame_index(self):
        """
        当前帧序号, 取人物动画的当前帧序号
        :return:
        """
        if self.child('char'):
            return self.child('char').frame_index
        return 0

    @frame_index.setter
    def frame_index(self, idx):
        self.child('char').frame_index = idx
        if self.child('weapon'):
            self.child('weapon').frame_index = idx

    @property
    def attack_frame(self):
        """
        攻击帧
        :return:
        """
        af, self.attack_acc, _ = get_model_attack_frame(self.model, get_weapon_type(self.weapon))
        # fr = self.frame_num // 2 + af[self.attack_stage]
        fr = [i + self.frame_num//2 for i in af]
        return fr

    def setup(self):
        self.setup_basic()
        self.setup_battle_unit()

    def setup_battle_unit(self):
        name = Label()
        name.text = self.name
        name.font_name = 'mod_AdobeSong.ttf'
        name.size = 16
        name.color = (0, 255, 0)
        name.shadow = True
        name.setup()
        self.add_child('name', name)

    def setup_basic(self):
        from Game.res_manager import fill_animation8d, fill_image_rect

        model_index = self.model
        weapon_index = ''
        if self.weapon and self.weapon != '' and get_weapon_type(self.weapon):
            model_index = self.model + '_' + get_weapon_type(self.weapon)
            weapon_index = self.weapon + "_" + self.model

        # self.clear_children(exception=['effect'])

        if model_index in self.shapes:
            ani_char = Animation8D()
            fill_animation8d(ani_char, self.shapes[model_index]['资源'], int(self.shapes[model_index][self.cur_action]))
            ani_char.set_fps(7)
            ani_char.direction = self.direction
            self.add_child('char', ani_char)
        else:
            print('shapes不存在5: ', self.model, model_index)
        if weapon_index and weapon_index != '':
            if weapon_index in self.shapes:
                ani_weapon = Animation8D()
                fill_animation8d(ani_weapon, self.shapes[weapon_index]['资源'], int(self.shapes[weapon_index][self.cur_action]))
                ani_weapon.set_fps(7)
                ani_weapon.direction = self.direction
                self.add_child('weapon', ani_weapon)
            else:
                print('shapes不存在6: ', model_index, weapon_index)

        shadow = ImageRect()
        fill_image_rect(shadow, 'shape.rsp', 0xDCE4B562)  # 3705976162
        self.add_child('shadow', shadow)

        self.attack_acc = get_model_attack_frame(self.model, get_weapon_type(self.weapon))[1]

        # if self.child('effect'):
        #     eff = self.child('effect')
        #     self.remove_child('effect')
        #     self.add_child('effect', eff)

    def update_battle_unit(self):
        if self.child('name'):
            self.child('name').center_x = self.x
            self.child('name').center_y = self.y + 20

    def update_basic(self):
        if self.child('char'):
            self.child('char').direction = self.direction
            self.cur_char_animation = self.child('char').cur_animation
        if self.child('weapon'):
            self.child('weapon').direction = self.direction

        # MaskRect
        if self.cur_char_animation and self.cur_char_animation.cur_frame:
            mask = pygame.mask.from_surface(self.cur_char_animation.cur_frame)
            self.mask_rect = mask.get_rect()
            self.mask_rect.x = self.x - self.cur_char_animation.kx
            self.mask_rect.y = self.y - self.cur_char_animation.ky

        if self.cur_char_animation:
            self.cur_char_animation.highlight = self.is_hover
        if self.cur_weapon_animation:
            self.cur_weapon_animation.highlight = self.is_hover

        if self.child('char'):
            self.child('char').is_playing = self.is_ani_playing
        if self.child('weapon'):
            self.child('weapon').is_playing = self.is_ani_playing

        # 染色
        if self.color_recipe != (0, 0, 0) and self.cur_char_animation and not self.cur_char_animation.is_modulated:
            from Game.res_manager import modulate_animation_by_palette
            wpal_file = '{}{}.wpal'.format(wpal_dir, self.model)
            if os.path.exists(wpal_file):
                if self.is_moving:
                    pal16 = self.child('char').palette16
                else:
                    pal16 = self.child('char').palette16
                try:
                    modulate_animation_by_palette(self.cur_char_animation, wpal_file, pal16, self.color_recipe)
                except:
                    self.cur_char_animation.is_modulated = True
            else:
                self.cur_char_animation.is_modulated = True
                print('染色文件不存在:', wpal_file)

        # 鼠标指向时指针变化
        if self.is_hover:
            if self.director.char_hover != self.id:
                self.director.char_hover = self.id
                if self.type == 'npc':
                    self.director.child('mouse').change_state('事件')
        else:
            if self.director.char_hover == self.id:
                self.director.char_hover = None
                if self.type == 'npc':
                    self.director.child('mouse').set_last_state()

        # 抖动
        if self.is_shaking and not self.path:
            dx, dy = random.randint(-1, 1), random.randint(-1, 1)
            self.x = self.tmp_x + dx
            self.y = self.tmp_y + dy
            if self.child('effect'):
                self.child('effect').x, self.child('effect').y = self.ori_x, self.ori_y

        # 部分动作到达最终帧后停止更新
        if self.cur_action in ['挨打', '防御', '死亡'] and self.reach_end_frame():
            self.is_ani_playing = False

        # 归位完成, 换动作'待战'
        if self.is_moving_back:
            if not self.path and not self.is_dead:
                self.change_action('待战')
                self.is_moving_back = False

        # 施法动作完成后, 换动作'待战'
        if self.cur_action == '施法':
            if self.reach_end_frame():
                self.change_action('待战')

        # 击退完成后自动归位
        if self.is_moving_backward == 1 and not self.path:
            self.move_back(1)
            self.is_moving_backward = 0
            if self.is_dead:
                self.change_action('死亡')

        # 特效播放完自动停止
        try:
            if self.child('effect').reach_end_frame():
                self.stop_effect()
        except BaseException:
            pass

    def change_action(self, act, sound=True):
        """
        更换动作
        :param act: ['攻击', '攻击2', '死亡', '防御', '待战', '施法', '奔跑', '挨打']
        :param sound: 是否播放音效
        :return:
        """
        self.is_ani_playing = True
        self.is_moving_backward = False  # 换动作则重置击退状态
        if act in ['攻击', '攻击2', '死亡', '防御', '待战', '施法', '奔跑', '挨打']:
            self.frame_index = 0
            if act == '攻击' or act == '攻击2':
                self.attack_stage = 0
            self.cur_action = act
            self.setup_basic()
            self.setup_battle_unit()

            if act in ['攻击', '攻击2', '死亡', '防御', '施法', '挨打'] and sound:
                play_char_sound(self.model.lstrip('进阶'), act.rstrip('2'))

            # 不同动作的FPS
            if act == '奔跑':
                self.set_fps(20)
            elif act == '攻击' or act == '攻击2':
                self.set_fps(10)
            elif act == '施法':
                self.set_fps(10)
            else:
                self.set_fps(7)

            if act == '挨打':  # 挨打动作时稍微移动
                self.is_moving_back = False
                if self.camp == OUR:
                    self.x -= 5
                    self.y -= 5
                else:
                    self.x += 5
                    self.y += 5

        self.frame_index = 0

    def move(self):
        target = self.path[0]
        # self.direction = calc_direction((self.ori_x, self.ori_y), target)
        vector = pygame.Vector2()
        vector.x, vector.y = int(target[0]) - self.x, int(target[1]) - self.y
        if vector.length() == 0:
            return
        vector.normalize_ip()
        vector.scale_to_length(self.moving_speed)
        self.x += vector.x
        self.y += vector.y
        self.tmp_x, self.tmp_y = self.x, self.y

    def update_path(self):
        if len(self.path) > 0:
            if self.clear_path:
                self.path = []
                self.clear_path = False
                self.is_moving = False
            else:
                self.is_moving = True
                _target = self.path[0]
                th = self.moving_speed // 2 + 1
                if abs(self.ori_x - int(_target[0])) <= th and abs(self.ori_y - int(_target[1])) <= th:
                    self.path.pop(0)
                else:
                    self.move()
        else:
            self.is_moving = False

    def move_backward(self, shaking=False, dis=MOVING_BACKWARD_DIS, death=False):
        """
        挨打被击退
        :param shaking: 抖动
        :param dis: 距离
        :param death: 是否死亡
        :return:
        """
        self.is_moving_backward = 1
        self.moving_speed = self.l_speed
        self.is_shaking = shaking
        self.is_dead = death
        if self.camp == OUR:
            self.path = [(self.x + dis, self.y + dis)]
        else:
            self.path = [(self.x - dis, self.y - dis)]

    def move_back(self, speed=0):
        """
        返回到ori_x, ori_y
        :param speed: 0:高速, 1:低速
        :return:
        """
        print('返回:', self.model)
        fps_scale = 1
        self.is_moving_backward = 0  # 返回时重置击退标志位
        # self.change_action('奔跑')
        self.is_shaking = False
        self.is_moving_back = True
        if speed == 0:
            self.moving_speed = self.h_speed
        else:
            self.moving_speed = self.l_speed * fps_scale
        self.path = [(self.ori_x, self.ori_y)]

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

    def reach_end_frame(self):
        """
        是否到达最后一帧
        :return:
        """
        if self.frame_index == self.frame_num - 1:
            # print('到最终帧:', self.model, self.frame_index, self.frame_num)
            return True
        else:
            return False

    def play_effect(self, name):
        if not name:
            name = '被击中'
        eff = MagicEffect(name)
        eff.x, eff.y = 0, 0
        fps_scale = get_magic_effect_fps_scale(name)
        eff.set_fps(int(fps_scale * EFFECT_FPS))
        self.add_child('effect', eff)
        self.child('effect').visible = True

    def stop_effect(self):
        # if self.child('effect'):
        #     self.remove_child('effect')
        self.child('effect').visible = False

    def add_buff(self, name):
        beff = BuffEffect(name)
        if beff.is_in_front:
            self.child('front_buff').add_child('name', beff)
        else:
            self.child('behind_buff').add_child('name', beff)
        if beff.is_on_top:
            # dy = self.child('char').height - 5
            dy = 75
            beff.y -= dy

    def remove_buff(self, name):
        self.child('front_buff').remove_child(name)
        self.child('behind_buff').remove_child(name)

    def update(self):
        self.update_path()
        self.update_basic()
        self.update_battle_unit()
