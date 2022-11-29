from Node.node import Node
from Node.button import Button
from Node.image_rect import ImageRect
from Node.progressbar import ProgressBar
from Common.common import *
from Database.map_name import get_map_name
from Node.label import Label
from Node.animation import Animation8D
import datetime
from Common.constants import *


class TimeArea(Node):
    def __init__(self):
        super(TimeArea, self).__init__()
        self.ch_hour_res = [0x361FA820, 0xC0A66903, 0xD1D11294, 0xAA7DEB05, 0x21274A87, 0x09C4978D, 0xC9E2F072,
                             0x2ACB36B2, 0xC26BF189, 0x1AA170AE, 0x7921D3A3, 0xEA7CAB84]  # 时辰素材
        self.ch_hour = 0  # 时辰, 0-11

        from Game.res_manager import fill_res
        白天背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                'hash_id': 0x9DF6DEBC,
                                                'top_left_x': 14,
                                                'top_left_y': 32})
        self.add_child('day_bg', 白天背景)
        self.child('day_bg').crop(0, 0, 80, 30)

        夜晚背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                'hash_id': 0x99738F4C,
                                                'top_left_x': 14,
                                                'top_left_y': 32})
        self.add_child('night_bg', 夜晚背景)
        self.child('night_bg').crop(0, 0, 80, 30)
        self.child('night_bg').enable = False

        背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                 'hash_id': 0xDE3F48B7,
                                                 'top_left_x': 0,
                                                 'top_left_y': 0})
        self.add_child('bg', 背景)

        走路小人 = set_node_attr(Animation8D(), {'rsp_file': 'wzife.rsp',
                                              'hash_id': 0xC7BEBF45,
                                              'top_left_x': 58,
                                              'top_left_y': 60})
        self.add_child('walker', 走路小人)

        奔跑小人 = set_node_attr(Animation8D(), {'rsp_file': 'wzife.rsp',
                                                  'hash_id': 0xAC307575,
                                                  'top_left_x': 58,
                                                  'top_left_y': 60})
        self.add_child('runner', 奔跑小人)
        self.child('runner').enable = False

        label_hms = Label()
        label_hms.size = 13
        label_hms.color = (255, 255, 255)
        label_hms.shadow = False
        label_hms.setup()
        self.add_child('label_hms', label_hms)

        label_map_name = Label()
        label_map_name.size = 14
        label_map_name.color = (255, 255, 255)
        label_map_name.shadow = True
        label_map_name.setup()
        self.add_child('label_map_name', label_map_name)

        label_xy = Label()
        label_xy.size = 14
        label_xy.color = (255, 255, 255)
        label_xy.shadow = False
        label_xy.setup()
        self.add_child('label_xy', label_xy)

        hour = ImageRect()
        self.add_child('ch_hour', hour)
        fill_res(self.child('ch_hour'), 'wzife.rsp', self.ch_hour_res[self.ch_hour])
        self.child('ch_hour').x, self.child('ch_hour').y = 1, 22

        fold = Button()
        self.add_child('btn_fold', fold)
        fill_res(self.child('btn_fold'), 'wzife.rsp', 0x6EDD4D71)
        self.child('btn_fold').x, self.child('btn_fold').y = 3, 64

        help = Button()
        self.add_child('btn_help', help)
        fill_res(self.child('btn_help'), 'wzife.rsp', 0xBAF6A95D)
        self.child('btn_help').x, self.child('btn_help').y = 99, 17

        world_map = Button()
        self.add_child('btn_world_map', world_map)
        fill_res(self.child('btn_world_map'), 'wzife.rsp', 0xBAF6A95D)
        self.child('btn_world_map').x, self.child('btn_world_map').y = 99, 35

        mini_map = Button()
        self.add_child('btn_mini_map', mini_map)
        fill_res(self.child('btn_mini_map'), 'wzife.rsp', 0xBAF6A95D)
        self.child('btn_mini_map').x, self.child('btn_mini_map').y = 99, 53

        introduction = Button()
        self.add_child('btn_introduction', introduction)
        fill_res(self.child('btn_introduction'), 'wzife2.rsp', 0xF102F42D)
        self.child('btn_introduction').x, self.child('btn_introduction').y = 1, 78

    def set_hour(self, h):
        """
        设置时辰
        :param h: 时辰数, 0-11
        :return:
        """
        from Game.res_manager import fill_res
        self.ch_hour = h
        fill_res(self.child('ch_hour'), 'wzife.rsp', self.ch_hour_res[self.ch_hour])

    def update(self):
        # 时分秒文本
        hms = datetime.datetime.now().strftime("%H:%M:%S")
        if self.child('label_hms').text != hms:
            self.child('label_hms').text = hms
            self.child('label_hms').setup()
        self.child('label_hms').center_x = 59
        self.child('label_hms').center_y = 10

        # 地图名称文本
        if game.world:
            map_id = game.world.map_id
            map_name = get_map_name(int(map_id))
            if self.child('label_map_name').text != map_name:
                self.child('label_map_name').text = map_name
                self.child('label_map_name').setup()
            self.child('label_map_name').center_x = 59
            self.child('label_map_name').center_y = 23

        # 坐标文本
        hero = game.hero
        if hero:
            text_xy = 'X:{} Y:{}'.format(str(int(hero.game_x)), str(int(hero.game_y)))
            if self.child('label_xy').text != text_xy:
                self.child('label_xy').text = text_xy
                self.child('label_xy').setup()
            self.child('label_xy').x = 24
            self.child('label_xy').center_y = 72

