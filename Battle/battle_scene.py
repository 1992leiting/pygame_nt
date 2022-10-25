import random

from Node.node import Node
from Node.character import BattleUnit, NPC
from Common.constants import *
import pygame
from Common.common import *
from Node.magic_effect import FullScreenEffect
from Node.label import Label
import time
from Node.magic_effect import MagicEffect
from Node.hp_effect import HpEffect


敌方位置 = {1: {"y": 188, "x": 347}, 3: {"y": 158, "x": 407}, 2: {"y": 218, "x": 287}, 4: {"y": 128, "x": 467}, 5: {"y": 248, "x": 227}, 6: {"y": 233, "x": 396}, 7: {"y": 263, "x": 341}, 8: {"y": 203, "x": 456}, 9: {"y": 173, "x": 516}, 10: {"y": 293, "x": 281}}
我方位置 = {1: {"y": 421, "x": 709}, 2: {"y": 451, "x": 649}, 3: {"y": 391, "x": 769}, 4: {"y": 481, "x": 589}, 5: {"y": 361, "x": 829}, 6: {"y": 355, "x": 635}, 7: {"y": 385, "x": 575}, 8: {"y": 325, "x": 695}, 9: {"y": 415, "x": 515}, 10: {"y": 295, "x": 755}}


my_units = [
    dict(名称='测试单位', 模型='大力金刚', 武器=''),
    dict(名称='测试单位', 模型='巨魔王', 武器='护法灭魔'),

    dict(名称='测试单位', 模型='虎头怪', 武器='震天锤'),
    dict(名称='测试单位', 模型='龙太子', 武器='秋水人家'),
    # dict(名称='测试单位', 模型='地狱战神', 武器=''),
    dict(名称='测试单位', 模型='剑侠客', 武器='四法青云'),
    # dict(名称='测试单位', 模型='飞燕女', 武器='赤焰双剑'),
    dict(名称='宝宝1号', 模型='古代瑞兽', 武器=''),
    dict(名称='宝宝2号', 模型='古代瑞兽', 武器=''),
    dict(名称='宝宝3号', 模型='古代瑞兽', 武器=''),
    dict(名称='宝宝4号', 模型='古代瑞兽', 武器=''),
    dict(名称='宝宝5号', 模型='古代瑞兽', 武器=''),
]


enemy_units = [
    # dict(名称='测试单位', 模型='虎头怪', 武器='鬼王蚀日'),
    dict(名称='测试单位', 模型='龙太子', 武器=' '),
    dict(名称='宝宝1号', 模型='剑侠客', 武器=''),
    dict(名称='测试单位', 模型='逍遥生', 武器='秋水人家'),
    dict(名称='测试单位', 模型='吸血鬼', 武器=''),
    dict(名称='测试单位', 模型='骨精灵', 武器='青刚刺'),
    # dict(名称='测试单位', 模型='龙太子', 武器='红缨枪'),
    dict(名称='宝宝1号', 模型='护卫', 武器=''),
    dict(名称='宝宝2号', 模型='护卫', 武器=''),
    dict(名称='宝宝3号', 模型='护卫', 武器=''),
    dict(名称='宝宝4号', 模型='护卫', 武器=''),
    dict(名称='宝宝5号', 模型='护卫', 武器=''),
]


class BattleScene(Node): 
    def __init__(self):
        super(BattleScene, self).__init__()
        self.ysort = True
        self.my_units = {}  # 我方战斗单位
        self.enemy_units = {}  # 敌方战斗单位
        self.plist = []  # 战斗流程列信息
        self.process = 0  # 当前战斗流程序号
        self.aunits = []  # 主动方, 第一个单位为攻击/施法者
        self.punits = []  # 被动方, 第一个单位为被动主要单位, 比如群法点选单位

        # units子节点和特效子节点, 设定好顺序防止覆盖关系错误
        self.add_child('units', Node())
        self.child('units').ysort = True
        self.add_child('full_screen_effect', Node())  # 全屏法术特效UI层
        self.add_child('hp_effect', Node())  # 掉血/加血特效UI层

        # 施法提示
        tip = Label()
        tip.text = ''
        tip.font_name = 'simsun.ttf'
        tip.size = 16
        tip.anti_aliased = True
        tip.color = (245, 222, 179)
        tip.setup()
        tip.time = time.time()
        self.add_child('spelling_tip', tip)

        self.setup_units()

    def play_effect(self, skill, x, y, name='effect'):
        """
        在战斗场景播放特效, 一般是坐标固定的特效, 比如反震
        :param skill: 技能/特效名称
        :param x: 坐标x
        :param y: 坐标y
        :param name: 子节点名称
        :return:
        """
        if not skill:
            skill = '被击中'
        eff = MagicEffect(skill)
        eff.x, eff.y = x, y
        fps_scale = get_magic_effect_fps_scale(skill)
        eff.set_fps(int(fps_scale * EFFECT_FPS))
        self.add_child(name, eff)

    def show_hp_effect(self, value, bu, hp_type=HP_DROP):
        """
        显示血量特效, child_name命名: hpe_dw_战斗单位编号(bu_index)
        :param value: 血量数值
        :param bu: 战斗单位
        :param hp_type: 掉血/加血
        :return:
        """
        hpe = HpEffect(value, hp_type)
        hpe.x, hpe.y = bu.x, bu.y - 40
        child_name = 'hpe_{}_{}'.format(bu.camp, bu.bu_index)
        # print('hp name:', child_name)
        self.child('hp_effect').add_child(child_name, hpe)

    def show_fullscreen_effect(self, name):
        self.child('full_screen_effect').visible = True
        feff = FullScreenEffect(name)
        if feff.black_bg:
            self.get_parent().child('black_mask').visible = True
        self.child('full_screen_effect').add_child('effect', feff)
        play_skill_effect_sound(name)

    def show_spelling_tip(self, name, skill_name, skill_type='法术'):
        self.child('spelling_tip').text = '{}使用了【{}】{}'.format(name, skill_type, skill_name)
        self.child('spelling_tip').setup()
        self.child('spelling_tip').center_x = self.director.window_w / 2
        self.child('spelling_tip').center_y = self.director.window_h - 80
        self.child('spelling_tip').visible = True
        self.child('spelling_tip').time = time.time()

    def setup_units(self):
        self.my_units = my_units
        self.enemy_units = enemy_units
        for i, unit in enumerate(self.my_units):
            num = i + 1
            bu = BattleUnit()
            bu.direction = 2
            bu.x, bu.y = 我方位置[num]['x'] - 120, 我方位置[num]['y']
            bu.ori_x, bu.ori_y = bu.x, bu.y
            bu.tmp_x, bu.tmp_y = bu.x, bu.y
            bu.camp = OUR
            bu.bu_index = i
            bu.set_data(unit)
            self.child('units').add_child('my_' + str(num), bu)

        for i, unit in enumerate(self.enemy_units):
            num = i + 1
            bu = BattleUnit()
            bu.direction = 0
            bu.x, bu.y = 敌方位置[num]['x'] - 120, 敌方位置[num]['y']
            bu.ori_x, bu.ori_y = bu.x, bu.y
            bu.tmp_x, bu.tmp_y = bu.x, bu.y
            bu.camp = OPPO
            bu.bu_index = i
            bu.set_data(unit)
            self.child('units').add_child('enemy_' + str(num), bu)

    def check_event(self):
        super(BattleScene, self).check_event()
        # test
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_1]):
            self.aunits = [self.child('units').child('my_1')]
            self.plist = [
                {'流程': 1, '返回': False, '技能名称': '破血狂攻', '目标单位': [1]},
                {'流程': 1, '返回': True, '技能名称': '破血狂攻', '目标单位': [1]},
                # {'流程': 50, '返回': True, '技能名称': '唧唧歪歪', '目标单位': [1, 2, 3, 4]},
                {'流程': 1, '返回': True, '技能名称': '', '目标单位': [1]},
            ]
            self.next_process(False)
        if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_2]):
            self.aunits = [self.child('units').child('my_2')]
            self.plist = [
                {'流程': 1, '返回': False, '技能名称': '连环击', '目标单位': [2]},
                {'流程': 1, '返回': False, '技能名称': '连环击', '目标单位': [2]},
                {'流程': 1, '返回': False, '技能名称': '连环击', '目标单位': [2]},
                {'流程': 1, '返回': False, '技能名称': '连环击', '目标单位': [2]},
                {'流程': 1, '返回': True, '技能名称': '连环击', '目标单位': [2]}
            ]
            self.next_process(False)
        if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_3]):
            self.aunits = [self.child('units').child('my_3')]
            self.plist = [
                {'流程': 1, '返回': True, '技能名称': '鹰击', '反震伤害': 120, '目标单位': [1]},
                {'流程': 1, '返回': True, '技能名称': '鹰击', '反震伤害': 120, '目标单位': [2]},
                {'流程': 1, '返回': True, '技能名称': '鹰击', '反震伤害': 120, '目标单位': [3]},
                {'流程': 1, '返回': True, '技能名称': '鹰击', '反震伤害': 120, '目标单位': [4]},
                {'流程': 1, '返回': True, '技能名称': '鹰击', '反震伤害': 120, '目标单位': [5]},
            ]
            self.next_process(False)
        if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_4]):
            self.aunits = [self.child('units').child('my_4')]
            self.plist = [
                # {'流程': 50, '返回': True, '技能名称': '龙腾', '目标单位': [4]},  # '龙卷雨击', '奔雷咒', '地狱烈火', '水漫金山', '泰山压顶'
                {'流程': 100, '返回': True, '技能名称': random.choice(['奔雷咒', '地狱烈火', '水漫金山', '泰山压顶']), '目标单位': random.sample(values, 5)},
            ]
            self.next_process(False)
        if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_5]):
            self.aunits = [self.child('units').child('my_5')]
            self.plist = [
                # {'流程': 1, '返回': True, '技能名称': '', '目标单位': [5]},
                {'流程': 1, '返回': False, '技能名称': '横扫千军', '反震伤害': 120, '目标单位': [4]},
                {'流程': 1, '返回': False, '技能名称': '横扫千军', '反震伤害': 120, '目标单位': [4]},
                {'流程': 1, '返回': True, '技能名称': '横扫千军', '反震伤害': 120, '目标单位': [4]},
            ]
            self.next_process(False)

        if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_6]):
            self.aunits = [self.child('units').child('my_4')]
            self.plist = [
                # {'流程': 1, '返回': True, '技能名称': '', '目标单位': [5]},
                {'流程': 50, '返回': False, '技能名称': '烈火', '目标单位': [4]},
            ]
            self.next_process(False)

        if self.director.match_kb_event(STOP, [pygame.KEYDOWN, pygame.K_7]):
            self.aunits = [self.child('units').child('my_4')]
            self.plist = [
                {'流程': 150, '返回': False, '技能名称': '推气过宫', '目标单位': [1, 2, 3, 5], '目标阵营': 0},
                {'流程': 50, '返回': False, '技能名称': '唧唧歪歪', '目标单位': [1, 2, 3, 5], '目标阵营': 1},
                {'流程': 1, '返回': False, '技能名称': '破血狂攻', '目标单位': [1]},
                {'流程': 1, '返回': True, '技能名称': '破血狂攻', '目标单位': [1]},
            ]
            self.next_process(False)

    def next_process(self, pop=True):
        """
        进行下一流程
        :param pop: 是否删除当前第一个流程()
        :return:
        """
        print('next process...', pop)
        if self.plist:
            if pop:
                self.plist.pop(0)  # 删除已经执行完的上一流程
            if self.plist:
                self.process = self.plist[0]['流程']  # 设置流程编号

                # 战斗施法提示
                if self.plist[0]['技能名称']:
                    # print('show tip:', self.plist[0]['技能名称'])
                    self.show_spelling_tip(self.aunits[0].name, self.plist[0]['技能名称'])

                # 指定被攻击单位
                self.punits = []
                if self.plist[0].get('目标阵营') == 0:
                    for pu_num in self.plist[0]['目标单位']:
                        pu = self.child('units').child('my_' + str(pu_num))
                        self.punits.append(pu)
                else:
                    for pu_num in self.plist[0]['目标单位']:
                        pu = self.child('units').child('enemy_' + str(pu_num))
                        self.punits.append(pu)
                return
        self.process = 0  # 如果没有下一流程, 则重置流程编号

    def update(self):
        # print('process: ', self.process)

        # 特效播放完成自动清除
        for child_name, child in self.get_children().copy().items():
            if type(child) == MagicEffect:
                if child.reach_end_frame():
                    self.remove_child(child_name)

        if time.time() - self.child('spelling_tip').time >= 2:
            self.child('spelling_tip').visible = False

        if not self.plist:
            return

        # 物理攻击开始流程
        if self.process == 1 and self.aunits and self.punits and self.aunits[0].cur_action == '待战':
            # 主动方移动
            self.aunits[0].path = [(self.punits[0].ori_x + 70, self.punits[0].ori_y + 70)]
            self.process = 2
        elif self.process == 2 and not self.aunits[0].path:
            # 主动方移动结束, 换动作'攻击'
            self.aunits[0].change_action('攻击')
            self.process = 3
        elif self.process == 3:
            stage = self.aunits[0].attack_stage
            shaking = False
            if len(self.aunits[0].attack_frame) > 1 and self.aunits[0].attack_frame[1] - self.aunits[0].attack_frame[0] > 2:
                shaking = True
            if self.aunits[0].reach_attack_frame():
                self.punits[0].is_shaking = shaking
                if stage == 0:
                    self.punits[0].change_action('挨打')
                    _skill = self.plist[0]['技能名称']
                    self.punits[0].play_effect(_skill)
                    if _skill:
                        play_skill_effect_sound(_skill)
            # 主动方没有下一段攻击, 进入下一个process
            if self.aunits[0].attack_stage == -1:
                self.punits[0].move_backward()
                if self.plist[0].get('反震伤害'):
                    self.aunits[0].change_action('挨打')
                    self.play_effect('反震', self.punits[0].x, self.punits[0].y, '反震')
                    self.show_hp_effect(random.randrange(200, 500), self.aunits[0])
                self.show_hp_effect(random.randrange(800, 2000), self.punits[0])
                self.process = 4
        elif self.process == 4:
            if not (self.child('反震') and self.child('反震').frame_index < 9):
                if self.aunits[0].reach_end_frame():
                    self.aunits[0].change_action('待战')
                    self.punits[0].backward_acc_cnt = 0
                    self.process = 5
        elif self.process == 5:
            self.aunits[0].change_action('待战')
            if self.plist[0]['返回']:
                self.aunits[0].move_back(0)
                self.process = 6
            else:
                self.next_process()
        elif self.process == 6:
            if not self.aunits[0].path:
                self.aunits[0].add_buff('后发制人')
                self.aunits[0].add_buff('红灯')
                self.next_process()

        # 法术攻击开始流程
        elif self.process == 50:
            self.aunits[0].change_action('施法')
            _skill = self.plist[0]['技能名称']
            for pu in self.punits:
                pu.play_effect(_skill)
                play_skill_effect_sound(_skill)
            self.process = 51
        elif self.process == 51:
            all_end = True  # 所有被动单位的法术特效都结束
            for pu in self.punits:
                eff = pu.child('effect')
                if eff:
                    stage = eff.attack_stage
                    shaking = False
                    if len(eff.attack_frame) > 1 and eff.attack_frame[1] - eff.attack_frame[0] > 2:
                        shaking = True
                    pu.is_shaking = shaking
                    if eff.reach_attack_frame():
                        if stage == 0:
                            pu.change_action('挨打', False)
                    if not eff.attack_stage == -1:  # 法术打击完成
                        all_end = False
                    else:
                        pu.change_action('挨打')
                        pu.move_backward()
                        self.show_hp_effect(random.randrange(800, 2000), pu)
                else:
                    all_end = False
            if all_end:
                self.process = 52
        elif self.process == 52:
            all_end = True  # 所有被动单位动作结束
            for pu in self.punits:
                eff = pu.child('effect')
                if not pu.path and eff.reach_end_frame():
                    pu.stop_effect()
                    pu.move_back(1)
                    pu.change_action('待战')
                else:
                    sall_end = False
            if all_end:
                self.next_process()

        # 全屏法术开始流程
        elif self.process == 100:
            self.aunits[0].change_action('施法')
            _skill = self.plist[0]['技能名称']
            self.show_fullscreen_effect(_skill)
            self.process = 101
        elif self.process == 101:
            _skill = self.plist[0]['技能名称']
            feff = self.child('full_screen_effect').child('effect')
            if feff and feff.reach_attack_frame():
                feff.visible = True
                shaking = False
                if len(feff.attack_frame) > 1 and feff.attack_frame[1] - feff.attack_frame[0] > 10:
                    shaking = True
                for pu in self.punits:
                    pu.is_shaking = shaking
                    if pu.cur_action != '挨打':
                        pu.change_action('挨打')
            if feff.attack_stage == -1:
                for pu in self.punits:
                    pu.move_backward()
                    self.show_hp_effect(random.randrange(800, 2000), pu)
                self.process = 102
        elif self.process == 102:
            feff = self.child('full_screen_effect').child('effect')
            if feff and feff.is_ended:
                self.child('full_screen_effect').visible = False
                self.get_parent().child('black_mask').visible = False
                self.process = 0

        # 法术恢复/BUFF/道具流程
        elif self.process == 150:
            self.aunits[0].change_action('施法')
            _skill = self.plist[0]['技能名称']
            for pu in self.punits:
                pu.play_effect(_skill)
                play_skill_effect_sound(_skill)
            self.process = 151
        elif self.process == 151:
            for pu in self.punits:
                eff = pu.child('effect')
                # 只要有一个被动单位法术到达指定帧，则所有单位添加血量特效
                if eff.frame_index == 5:
                    for _pu in self.punits:
                        self.show_hp_effect(random.randrange(400, 450), _pu, HP_RECOVER)
                    self.process= 152
                    break
        elif self.process == 152:
            all_end = True  # 所有被动单位动作结束
            for pu in self.punits:
                eff = pu.child('effect')
                if not pu.path and eff.reach_end_frame():
                    pu.stop_effect()
                else:
                    all_end = False
            if not self.aunits[0].cur_action == '待战':
                all_end = False
            if all_end:
                self.next_process()
