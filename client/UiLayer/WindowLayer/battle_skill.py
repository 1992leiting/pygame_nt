from UiLayer.WindowLayer.window_layer import Window
from Node.text_edit import LineEditWithBg
from Node.button import ButtonClassicRed
from Node.label import Label
from Common.socket_id import *
from Common.constants import *
from Node.object_block import SkillBlock


class BattleSkill(Window):
    def __init__(self):
        super(BattleSkill, self).__init__()
        self.enable = False
        self.window_title = '战斗技能栏'
        self.has_title_ui = False
        self.width, self.height = 190, 308
        self.config_file = winconfig_dir + 'BattleSkill.csv'
        self.skills = []  # 战斗中的主动技能
        self.setup()
        self.setup_win_config()

    def setup(self):
        super().setup()

    def setup_skills(self, skills:list):
        self.skills = skills
        for i, skill in enumerate(self.skills):
            self.child('skill_'+str(i)).setup(skill)

    def setup_win_config(self, file=None, given_node=None):
        super().setup_win_config()
        _x, _y = 27, 28
        _w, _h = 88, 42
        index = 0
        for i in range(5):
            for j in range(2):
                skill = SkillBlock()
                skill.x, skill.y = _x, _y
                print(_x, _y)
                self.add_child('skill_' + str(index), skill)
                _x += _w
                index += 1
            _x = 27
            _y += _h