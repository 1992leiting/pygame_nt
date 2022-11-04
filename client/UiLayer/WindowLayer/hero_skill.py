from UiLayer.WindowLayer.window_layer import Window
from UiLayer.WindowLayer.win_config import WinHeroAttr
from Common.constants import *
from Node.node import Node
from Node.button import ToggleButtonGroup, ButtonClassicRed
from Common.common import set_node_attr


config_smskill = winconfig_dir + 'HeroSkill_smskill.csv'
config_fzskill = winconfig_dir + 'HeroSkill_fzskill.csv'
config_jqskill = winconfig_dir + 'HeroSkill_jqskill.csv'
config_xlskill = winconfig_dir + 'HeroSkill_xlskill.csv'
config_jmskill = winconfig_dir + 'HeroSkill_jmskill.csv'


class HeroSkill(Window):
    def __init__(self):
        super(HeroSkill, self).__init__()
        self.window_title = '主 技 能'
        self.width, self.height = 452, 464
        self.btn_group = ToggleButtonGroup()
        self.add_child('btn_group', self.btn_group)

        self.config_file = config_smskill
        self.setup()
        self.setup_win_config(given_node=self.child('info_area'))

    def switch(self, visible):
        self.visible = visible
        self.child('info_area').clear_children()
        # self.setup()
        self.setup_win_config(given_node=self.child('info_area'))

    def setup(self):
        super(HeroSkill, self).setup()
        btn = set_node_attr(ButtonClassicRed(), {
            'x': 25,
            'y': 30,
            'width': 70,
            'text': '师门技能',
            'toggle_mode': True,
        })
        self.btn_group.append(btn)
        btn.setup()
        self.add_child('btn_师门技能', btn)

        btn = set_node_attr(ButtonClassicRed(), {
            'x': 108,
            'y': 30,
            'width': 70,
            'text': '辅助技能',
            'toggle_mode': True,
        })
        self.btn_group.append(btn)
        btn.setup()
        self.add_child('btn_辅助技能', btn)

        btn = set_node_attr(ButtonClassicRed(), {
            'x': 191,
            'y': 30,
            'width': 70,
            'text': '剧情技能',
            'toggle_mode': True,
        })
        self.btn_group.append(btn)
        btn.setup()
        self.add_child('btn_剧情技能', btn)

        btn = set_node_attr(ButtonClassicRed(), {
            'x': 274,
            'y': 30,
            'width': 70,
            'text': '修炼技能',
            'toggle_mode': True,
        })
        self.btn_group.append(btn)
        btn.setup()
        self.add_child('btn_修炼技能', btn)

        btn = set_node_attr(ButtonClassicRed(), {
            'x': 357,
            'y': 30,
            'width': 70,
            'text': '经脉技能',
            'toggle_mode': True,
        })
        self.btn_group.append(btn)
        btn.setup()
        self.add_child('btn_经脉技能', btn)

        self.add_child('info_area', Node())  # 该区域会随着按钮点击变化内容

    def check_event(self):
        super(HeroSkill, self).check_event()
        if self.child('btn_师门技能') and self.child('btn_师门技能').event:
            self.config_file = config_smskill
            self.child('info_area').clear_children()
            self.setup_win_config(given_node=self.child('info_area'))
        if self.child('btn_辅助技能') and self.child('btn_辅助技能').event:
            self.config_file = config_fzskill
            self.child('info_area').clear_children()
            self.setup_win_config(given_node=self.child('info_area'))
        if self.child('btn_剧情技能') and self.child('btn_剧情技能').event:
            self.config_file = config_jqskill
            self.child('info_area').clear_children()
            self.setup_win_config(given_node=self.child('info_area'))
        if self.child('btn_修炼技能') and self.child('btn_修炼技能').event:
            self.config_file = config_xlskill
            self.child('info_area').clear_children()
            self.setup_win_config(given_node=self.child('info_area'))
        if self.child('btn_经脉技能') and self.child('btn_经脉技能').event:
            self.config_file = config_jmskill
            self.child('info_area').clear_children()
            self.setup_win_config(given_node=self.child('info_area'))
