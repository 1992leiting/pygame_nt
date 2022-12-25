import random

from Node.node import Node
from Node.character import BattleUnit, NPC
from Common.constants import *
import pygame
from Common.common import *
from Common.socket_id import *
from Node.magic_effect import FullScreenEffect
from Node.label import Label
import time
from Node.magic_effect import MagicEffect
from Node.hp_effect import HpEffect
from Node.animation import Animation8D
from Node.image_rect import ImageRect
from Game.res_manager import fill_res
from Battle.cmd_menu import BattleCmdMenu


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


empty_cmd = dict(类型=None, 目标=None, 阵营=None, 参数=None, 附加=None)


class BattleScene(Node): 
    def __init__(self):
        super(BattleScene, self).__init__()
        self.ysort = True
        self.camp = 0  # 阵营为0则0-9在观战方/10-19在对战方, 阵营为1则相反
        self.my_units = {}  # 我方战斗单位
        self.enemy_units = {}  # 敌方战斗单位
        self.plist = []  # 战斗流程列信息
        self.status = ST_人物命令
        self.process = 0  # 当前战斗流程序号
        self.units0 = []  # 主动方, 第一个单位为攻击/施法者
        self.units1 = []  # 被动方, 第一个单位为被动主要单位, 比如群法点选单位
        self.battle_cmd = {ST_人物命令: empty_cmd.copy(), ST_召唤兽命令: empty_cmd.copy()}  # 人物和召唤兽的战斗命令
        self.setup_ui()

    def setup_ui(self):
        # 地图背景
        self.add_child('map_jpg', ImageRect())
        # 纯色背景(战斗)
        node = ImageRect().from_color((15, 25, 60, 190))
        # node.x, node.y = game.camera.x, game.camera.y
        self.add_child('grey_mask', node)
        # 黑色背景(战斗)
        node = ImageRect().from_color((0, 0, 0, 255))
        # node.x, node.y = game.camera.x, game.camera.y
        node.visible = False
        self.add_child('black_mask', node)
        # 法阵圆圈(战斗)
        node = Animation8D()
        fill_res(node, 'addon.rsp', 0xE3B87E0F)
        # node.x, node.y = 0, 200
        self.add_child('circle_mask', node)

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

        # 命令按钮
        self.add_child('cmd_menu', BattleCmdMenu())

    def reset_cmd(self):
        self.battle_cmd = {ST_人物命令: empty_cmd.copy(), ST_召唤兽命令: empty_cmd.copy()}  # 人物和召唤兽的战斗命令

    def set_battle_cmd(self, tp=None, target=None, camp=None, param=None, add=None):
        """
        设置战斗命令
        """
        if tp :
            self.battle_cmd[self.status]['类型'] = tp
        if target :
            self.battle_cmd[self.status]['目标'] = target
        if camp :
            self.battle_cmd[self.status]['阵营'] = camp
        if param :
            self.battle_cmd[self.status]['参数'] = param
        if add :
            self.battle_cmd[self.status]['附加'] = add

    def next_status(self):
        if self.status == ST_人物命令:
            self.status = ST_召唤兽命令
        elif self.status == ST_召唤兽命令:
            self.status = ST_等待状态
            send(C_战斗命令, self.battle_cmd)

    def set_unit_hp_data(self, battle_id, hp_data):
        unit = self.unit(battle_id)
        # 人物气血条
        unit.update_hp_bar(hp_data[0]['气血'], hp_data[0]['最大气血'])

    def enter_battle_scene(self):
        play_battle_music('战斗BOSS1')
        game.mouse.change_state('普通')
        map_jpg = ImageRect()
        map_jpg.image = game.world.child('map_jpg').image
        self.add_child('map_jpg', map_jpg)
        self.child('map_jpg').x, self.child('map_jpg').y = -game.camera.x, -game.camera.y

    def play_effect(self, skill, x, y, name='effect'):
        """
        在战斗场景播放特效, 一般是坐标固定位置的特效, 比如反震
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

    def show_hp_animation(self, value, bu, hp_type=DAMAGE):
        """
        显示血量特效, child_name命名: hpe_dw_战斗单位编号(bu_index)
        :param value: 血量数值
        :param bu: 战斗单位
        :param hp_type: 掉血/加血
        :return:
        """
        # 加血/掉血并刷新血条
        if hp_type == DAMAGE:
            bu.hp_current -= value
        else:
            bu.hp_current += value
        bu.update_hp_bar(bu.hp_current, bu.hp_max)
        # 显示血量动画
        hpe = HpEffect(value, hp_type)
        hpe.x, hpe.y = bu.x, bu.y - 40
        child_name = 'hpe_{}_{}'.format(bu.camp, bu.bu_index)
        self.child('hp_effect').add_child(child_name, hpe)

    def show_fullscreen_effect(self, name):
        self.child('full_screen_effect').visible = True
        feff = FullScreenEffect(name)
        if feff.black_bg:
            self.child('black_mask').visible = True
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
        print('setup units:', self.camp)
        self.child('units').clear_children()
        if self.camp == 0:
            for i in range(0, 10):
                unit = game.director.battle_units[str(i)]
                if unit:
                    print('my units:', unit['名称'])
                    num = i + 1
                    bu = BattleUnit()
                    bu.set_data(unit)
                    bu.battle_unit_id = i
                    bu.direction = 2
                    bu.x, bu.y = 我方位置[num]['x'] - 120, 我方位置[num]['y']
                    bu.ori_px, bu.ori_py = bu.x, bu.y
                    bu.tmp_x, bu.tmp_y = bu.x, bu.y
                    bu.camp = NEAR  # 我方单位
                    bu.bu_index = i
                    bu.left_click_callback = self.on_unit_left_click  # 点击单位回调函数
                    bu.right_click_callback = self.on_unit_right_click
                    self.child('units').add_child('unit_' + str(i), bu)

            for i in range(10, 20):
                unit = game.director.battle_units[str(i)]
                if unit:
                    print('enemy units:', unit['名称'])
                    num = i - 10 + 1
                    bu = BattleUnit()
                    bu.set_data(unit)
                    bu.battle_unit_id = i
                    bu.direction = 0
                    bu.x, bu.y = 敌方位置[num]['x'] - 120, 敌方位置[num]['y']
                    bu.ori_px, bu.ori_py = bu.x, bu.y
                    bu.tmp_x, bu.tmp_y = bu.x, bu.y
                    bu.camp = FAR  # 敌方单位
                    bu.bu_index = i
                    bu.left_click_callback = self.on_unit_left_click  # 点击单位回调函数
                    bu.right_click_callback = self.on_unit_right_click
                    self.child('units').add_child('unit_' + str(i), bu)
        else:
            for i in range(0, 10):
                unit = game.director.battle_units[str(i)]
                if unit:
                    print('enemy units:', unit['名称'])
                    num = i + 1
                    bu = BattleUnit()
                    bu.set_data(unit)
                    bu.battle_unit_id = i
                    bu.direction = 0
                    bu.x, bu.y = 敌方位置[num]['x'] - 120, 敌方位置[num]['y']
                    bu.ori_px, bu.ori_py = bu.x, bu.y
                    bu.tmp_x, bu.tmp_y = bu.x, bu.y
                    bu.camp = FAR
                    bu.bu_index = i
                    bu.left_click_callback = self.on_unit_left_click  # 点击单位回调函数
                    bu.right_click_callback = self.on_unit_right_click
                    self.child('units').add_child('unit_' + str(i), bu)

            for i in range(10, 20):
                unit = game.director.battle_units[str(i)]
                if unit:
                    print('my units:', unit['名称'])
                    num = i - 10 + 1
                    bu = BattleUnit()
                    bu.set_data(unit)
                    bu.battle_unit_id = i
                    bu.direction = 2
                    bu.x, bu.y = 我方位置[num]['x'] - 120, 我方位置[num]['y']
                    bu.ori_px, bu.ori_py = bu.x, bu.y
                    bu.tmp_x, bu.tmp_y = bu.x, bu.y
                    bu.camp = NEAR
                    bu.bu_index = i
                    bu.left_click_callback = self.on_unit_left_click  # 点击单位回调函数
                    bu.right_click_callback = self.on_unit_right_click
                    self.child('units').add_child('unit_' + str(i), bu)

    def on_unit_left_click(self, unit_id):
        print('点击BU:', unit_id)
        if self.status not in [ST_人物命令, ST_召唤兽命令]:
            return
        if not self.battle_cmd[self.status]['类型']:
            self.set_battle_cmd(tp='攻击')
        self.set_battle_cmd(target=unit_id)
        game.mouse.set_last_state()
        self.next_status()

    def on_unit_right_click(self, unit_id):
        pass

    def on_battle_skill_left_click(self, skill_name):
        print('点击技能:', skill_name)
        game.window_layer.switch_window('战斗技能栏', False)
        game.mouse.change_state('道具')
        self.set_battle_cmd(tp='法术', param=skill_name)

    def check_event(self):
        super(BattleScene, self).check_event()

    def unit(self, index):
        bu = self.child('units').child('unit_' + str(index))
        if not bu:
            print('BU为空:', index)
        return bu

    def unit_remove_buff(self, unit_id, name):
        self.unit(unit_id).remove_buff(name)

    def all_process_end(self):
        self.process = 0
        self.status = ST_等待状态
        send(C_战斗回合执行完成, {})

    def next_process(self, pop=True):
        """
        进行下一流程
        :param pop: 是否删除当前第一个流程()
        :return:
        """
        print('next process...', self.plist)
        self.status = ST_执行状态
        if self.plist:
            if pop:
                self.plist.pop(0)  # 删除已经执行完的上一流程
            if self.plist:
                self.process = self.plist[0]['流程']  # 设置流程编号

                self.units0 = [self.unit(self.plist[0]['攻击方'])]
                # 战斗施法提示
                if gdv(self.plist[0], '技能名称'):
                    # print('show tip:', self.plist[0]['技能名称'])
                    self.show_spelling_tip(self.units0[0].name, gdv(self.plist[0], '技能名称'))

                # 指定被攻击单位
                self.units1 = []
                for target in self.plist[0]['目标单位']:
                    target_id = target['编号']
                    pu = self.unit(target_id)
                    self.units1.append(pu)
                return
            else:
                self.all_process_end()
        else:
            self.all_process_end()

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
        if self.process == 1 and self.units0 and self.units1 and self.units0[0].cur_action in ['待战', '死亡']:
            # 主动方移动
            self.units0[0].set_speed(1)
            if self.units1[0].camp == FAR:
                self.units0[0].path = [(self.units1[0].ori_px + 70, self.units1[0].ori_py + 50)]
            else:
                self.units0[0].path = [(self.units1[0].ori_px - 70, self.units1[0].ori_py - 50)]
            self.process = 2
        elif self.process == 2 and not self.units0[0].path:
            # 主动方移动结束, 换动作'攻击'
            self.units0[0].change_action('攻击')
            self.process = 3
        elif self.process == 3:
            stage = self.units0[0].attack_stage
            shaking = False
            if len(self.units0[0].attack_frame) > 1 and self.units0[0].attack_frame[1] - self.units0[0].attack_frame[0] > 2:
                shaking = True
            if self.units0[0].reach_attack_frame():
                self.units1[0].is_shaking = shaking
                if stage == 0:
                    self.units1[0].change_action('挨打')
                    _skill = self.plist[0]['目标单位'][0]['特效']
                    self.units1[0].play_effect(_skill)
                    if _skill:
                        play_skill_effect_sound(_skill)
                    _crit = gdv(self.plist[0]['目标单位'][0]['伤害'], '必杀')
                    if _crit:
                        self.units1[0].play_effect('暴击')
            # 主动方没有下一段攻击, 进入下一个process
            if self.units0[0].attack_stage == -1:
                self.units1[0].move_backward(death=self.plist[0]['目标单位'][0]['死亡'])
                if self.plist[0].get('反震伤害'):
                    self.units0[0].change_action('挨打')
                    self.play_effect('反震', self.units1[0].x, self.units1[0].y, '反震')
                    self.show_hp_animation(self.plist[0]['反震伤害']['数值'], self.units0[0])
                if gdv(self.plist[0], '结尾掉血'):
                    self.show_hp_animation(gdv(self.plist[0], '结尾掉血'), self.units0[0])
                if gdv(self.plist[0], '添加状态'):
                    self.units0[0].add_buff(gdv(self.plist[0], '添加状态'))
                self.show_hp_animation(self.plist[0]['目标单位'][0]['伤害']['数值'], self.units1[0], self.plist[0]['目标单位'][0]['伤害']['类型'])
                self.process = 4
        elif self.process == 4:
            if not (self.child('反震') and self.child('反震').frame_index < 9):
                if self.units0[0].reach_end_frame():
                    self.units0[0].change_action('待战')
                    self.units1[0].backward_acc_cnt = 0
                    self.process = 5
        elif self.process == 5:
            self.units0[0].change_action('待战')
            if gdv(self.plist[0], '返回'):
                self.units0[0].move_back(0)
                self.process = 6
            else:
                if self.units0[0].action_end and self.units1[0].action_end:
                    self.next_process()
        elif self.process == 6:
            if self.units0[0].action_end and self.units1[0].action_end:
                self.next_process()

        # 法术攻击开始流程
        elif self.process == 50:
            self.units0[0].change_action('施法')
            _skill = self.plist[0]['技能名称']
            for pu in self.units1:
                pu.play_effect(_skill)
                play_skill_effect_sound(_skill)
            self.process = 51
        elif self.process == 51:
            all_end = True  # 所有被动单位的法术特效都结束
            for pu in self.units1:
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
                        self.show_hp_animation(random.randrange(800, 2000), pu)
                else:
                    all_end = False
            if all_end:
                self.process = 52
        elif self.process == 52:
            all_end = True  # 所有被动单位动作结束
            for pu in self.units1:
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
            self.units0[0].change_action('施法')
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
                for pu in self.units1:
                    pu.is_shaking = shaking
                    if pu.cur_action != '挨打':
                        pu.change_action('挨打')
            if feff.attack_stage == -1:
                for pu in self.units1:
                    pu.move_backward()
                    self.show_hp_animation(random.randrange(800, 2000), pu)
                self.process = 102
        elif self.process == 102:
            feff = self.child('full_screen_effect').child('effect')
            if feff and feff.is_ended:
                self.child('full_screen_effect').visible = False
                self.child('black_mask').visible = False
                self.process = 0

        # 法术恢复/BUFF/道具流程
        elif self.process == 150:
            self.units0[0].change_action('施法')
            _skill = self.plist[0]['技能名称']
            for pu in self.units1:
                pu.play_effect(_skill)
                play_skill_effect_sound(_skill)
            self.process = 151
        elif self.process == 151:
            for pu in self.units1:
                eff = pu.child('effect')
                # 只要有一个被动单位法术到达指定帧，则所有单位添加血量特效
                if eff.frame_index == 5:
                    for _pu in self.units1:
                        self.show_hp_animation(random.randrange(400, 450), _pu, RECOVER)
                    self.process= 152
                    break
        elif self.process == 152:
            all_end = True  # 所有被动单位动作结束
            for pu in self.units1:
                eff = pu.child('effect')
                if not pu.path and eff.reach_end_frame():
                    pu.stop_effect()
                else:
                    all_end = False
            if not self.units0[0].cur_action == '待战':
                all_end = False
            if all_end:
                self.next_process()

        # 取消法术状态
        elif self.process == 500:
            buff_name = self.plist[0]['buff名称']
            target = self.plist[0]['攻击方']
            self.unit(target).remove_buff(buff_name)
            self.next_process()
