from UiLayer.WindowLayer.window_layer import Window
from UiLayer.WindowLayer.win_config import WinHeroAttr
from Common.constants import *
from Common.socket_id import *


class HeroAttr(Window):
    def __init__(self):
        super(HeroAttr, self).__init__()
        self.enable = False
        self.window_title = '人物状态'
        self.width, self.height = 258, 454
        self.x = self.director.window_w - self.width
        self.config_file = winconfig_dir + 'HeroAttr.csv'
        self.setup()
        self.setup_win_config()
        self.top_right_x = game.director.window_w - 1

    def update(self):
        super(HeroAttr, self).update()
        self.child('le_名称').set_text(game.director.hero_data['名称'])
        self.child('le_级别').set_text(game.director.hero_data['等级'])
        self.child('le_称谓').set_text(game.director.hero_data['当前称谓'])
        self.child('le_帮派').set_text(game.director.hero_data['帮派'])
        self.child('le_门派').set_text(game.director.hero_data['门派'])
        self.child('le_帮贡').set_text(game.director.hero_data['帮贡'])
        self.child('le_人气').set_text(game.director.hero_data['人气'])
        self.child('le_贡献').set_text(game.director.hero_data['门贡'])
        self.child('le_命中').set_text(game.director.hero_data['命中'])
        self.child('le_伤害').set_text(game.director.hero_data['伤害'])
        self.child('le_防御').set_text(game.director.hero_data['防御'])
        self.child('le_速度').set_text(game.director.hero_data['速度'])
        self.child('le_法伤').set_text(game.director.hero_data['法伤属性'])
        self.child('le_法防').set_text(game.director.hero_data['法防属性'])
        self.child('le_体质').set_text(game.director.hero_data['体质'])
        self.child('le_魔力').set_text(game.director.hero_data['魔力'])
        self.child('le_力量').set_text(game.director.hero_data['力量'])
        self.child('le_耐力').set_text(game.director.hero_data['耐力'])
        self.child('le_敏捷').set_text(game.director.hero_data['敏捷'])
        self.child('le_潜力').set_text(game.director.hero_data['潜力'])
        self.child('le_升级经验').set_text(CHAR_LEVEL_EXP_REQ[int(game.director.hero_data['等级'])])
        self.child('le_获得经验').set_text(game.director.hero_data['当前经验'])
        text = '{}/{}/{}'.format(game.director.hero_data['气血'],
                                 game.director.hero_data['最大气血']-game.director.hero_data['伤势'],
                                 game.director.hero_data['最大气血'])
        self.child('气血').set_text(text)
        text = '{}/{}'.format(game.director.hero_data['魔法'], game.director.hero_data['最大魔法'])
        self.child('魔法').set_text(text)
        text = '{}/{}'.format(game.director.hero_data['愤怒'], 150)
        self.child('愤怒').set_text(text)
        text = '{}/{}'.format(game.director.hero_data['活力'], game.director.hero_data['最大活力'])
        self.child('活力').set_text(text)
        text = '{}/{}'.format(game.director.hero_data['体力'], game.director.hero_data['最大体力'])
        self.child('体力').set_text(text)

    def check_event(self):
        super(HeroAttr, self).check_event()
        if self.child('btn_技能') and self.child('btn_技能').event:
            self.win_manager.switch_window('人物技能')
        if self.child('btn_升级') and self.child('btn_升级').event:
            game.director.client.send(C_角色升级, {})
