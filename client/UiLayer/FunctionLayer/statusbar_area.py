from Node.node import Node
from Node.button import Button
from Node.image_rect import ImageRect
from Node.progressbar import ProgressBar
from Common.common import *
from Game.res_manager import fill_res
from Common.constants import *


class StatusbarArea(Node):
    def __init__(self):
        super(StatusbarArea, self).__init__()

        self.人物头像背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                 'hash_id': 906724211,
                                                 'x': self.director.window_w - 117,
                                                 'y': 0})
        self.add_child('人物头像背景', self.人物头像背景)
        self.人物气血空槽 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                      'hash_id': 780622062,
                                                      'x': self.director.window_w - 67,
                                                      'y': 0})
        self.add_child('人物气血空槽', self.人物气血空槽)
        self.人物伤势 = set_node_attr(ProgressBar(), {'rsp_file': 'wzife.rsp',
                                                      'hash_id': 9184785,
                                                      'x': self.director.window_w - 55,
                                                      'y': 2})
        self.add_child('人物伤势', self.人物伤势)
        # self.人物伤势.progress = 80
        self.人物气血条 = set_node_attr(ProgressBar(), {'rsp_file': 'wzife.rsp',
                                                        'hash_id': 2866038147,
                                                        'x': self.director.window_w - 55,
                                                        'y': 2})
        self.add_child('人物气血条', self.人物气血条)
        self.child('人物气血条').set_ratio(50, 100)
        self.人物气魔法空槽 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                      'hash_id': 780622062,
                                                      'x': self.director.window_w - 67,
                                                      'y': 12})
        self.add_child('人物气魔法空槽', self.人物气魔法空槽)
        self.人物魔法条 = set_node_attr(ProgressBar(), {'rsp_file': 'wzife.rsp',
                                                   'hash_id': 3461168173,
                                                   'x': self.director.window_w - 55,
                                                   'y': 14})
        self.add_child('人物魔法条', self.人物魔法条)
        self.人物气愤怒空槽 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                       'hash_id': 780622062,
                                                       'x': self.director.window_w - 67,
                                                       'y': 24})
        self.add_child('人物气愤怒空槽', self.人物气愤怒空槽)
        self.人物愤怒条 = set_node_attr(ProgressBar(), {'rsp_file': 'wzife.rsp',
                                                   'hash_id': 3136815263,
                                                   'x': self.director.window_w - 55,
                                                   'y': 26})
        self.add_child('人物愤怒条', self.人物愤怒条)
        self.人物气经验空槽 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                       'hash_id': 780622062,
                                                       'x': self.director.window_w - 67,
                                                       'y': 36})
        self.add_child('人物气经验空槽', self.人物气经验空槽)
        self.人物经验条 = set_node_attr(ProgressBar(), {'rsp_file': 'wzife.rsp',
                                                   'hash_id': 2067532004,
                                                   'x': self.director.window_w - 55,
                                                   'y': 38})
        self.add_child('人物经验条', self.人物经验条)
        self.人物头像 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                                 'hash_id': 3615876352,
                                                 'x': self.director.window_w - 114,
                                                 'y': 3})
        hero_model = game.director.hero_data['模型']
        has, rsp = head_image[hero_model]['小头像'], head_image[hero_model]['大头像文件']
        fill_res(self.人物头像, rsp, has)
        self.add_child('人物头像', self.人物头像)
        self.宠物气血空槽 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                      'hash_id': 780622062,
                                                      'x': self.director.window_w - 183,
                                                      'y': 0})
        self.add_child('宠物气血空槽', self.宠物气血空槽)
        self.宠物魔法空槽 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                      'hash_id': 780622062,
                                                      'x': self.director.window_w - 183,
                                                      'y': 12})
        self.add_child('宠物魔法空槽', self.宠物魔法空槽)
        self.宠物经验空槽 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                      'hash_id': 780622062,
                                                      'x': self.director.window_w - 183,
                                                      'y': 24})
        self.add_child('宠物经验空槽', self.宠物经验空槽)
        self.宠物气血条 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                  'hash_id': 2866038147,
                                                  'x': self.director.window_w - 171,
                                                  'y': 2})
        self.add_child('宠物气血条', self.宠物气血条)
        self.宠物魔法条 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                  'hash_id': 3461168173,
                                                  'x': self.director.window_w - 171,
                                                  'y': 14})
        self.add_child('宠物魔法条', self.宠物魔法条)
        self.宠物经验条 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                  'hash_id': 2067532004,
                                                  'x': self.director.window_w - 171,
                                                  'y': 26})
        self.add_child('宠物经验条', self.宠物经验条)
        self.宠物头像背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                                      'hash_id': 909815579,
                                                      'x': self.director.window_w - 220,
                                                      'y': 0})
        self.add_child('宠物头像背景', self.宠物头像背景)
        self.宠物头像 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                                 'hash_id': 3469228247,
                                                 'x': self.director.window_w - 218,
                                                 'y': 3})
        self.add_child('宠物头像', self.宠物头像)
