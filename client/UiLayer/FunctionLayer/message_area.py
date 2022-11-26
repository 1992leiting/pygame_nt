from Node.node import Node
from Node.image_rect import ImageRect
from Node.button import Button
from Node.animation import Animation8D
from Node.rich_text import RichText
from Node.text_edit import *
from Common.common import *
from Common.constants import *
from Common.socket_id import *


class MessageArea(Node):
    def __init__(self):
        from Game.res_manager import fill_res
        super(MessageArea, self).__init__()

        from Game.res_manager import fill_res
        聊天区背景 = ImageRect().from_img_file(pic_dir + 'blue_bg.png')
        聊天区背景.image = auto_sizing(聊天区背景.image, 418, 150)
        聊天区背景.width, 聊天区背景.height = 418, 150
        聊天区背景.bottom_left_x, 聊天区背景.bottom_left_y = 2, self.director.window_h - 25
        聊天区背景.setup_outline()
        self.add_child('聊天区背景', 聊天区背景)

        输入框背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife1.rsp',
                                           'hash_id': 1271218547,
                                           'bottom_left_x': 0,
                                           'bottom_left_y': self.director.window_h - 1})
        self.add_child('输入框背景', 输入框背景)

        # 输入框背景2 = set_node_attr(ImageRect(), {'rsp_file': 'wzife1.rsp',
        #                                     'hash_id': 1271218547,
        #                                     'bottom_left_x': 40,
        #                                     'bottom_left_y': self.director.window_h - 1})
        输入框背景2 = ImageRect()
        fill_res(输入框背景2, 'wzife1.rsp', 1271218547)
        输入框背景2.image = auto_sizing(输入框背景2.image, 335, 23)
        输入框背景2.width, 输入框背景2.height = 335, 23
        输入框背景2.bottom_left_x, 输入框背景2.bottom_left_y = 83, self.director.window_h - 1
        self.add_child('输入框背景2', 输入框背景2)

        btn_当前频道 = set_node_attr(Button(), {'rsp_file': 'wzife.rsp',
                                            'hash_id': 1056875442,
                                            'bottom_left_x': 0,
                                            'bottom_left_y': self.director.window_h - 1})
        self.add_child('btn_当前频道', btn_当前频道)

        频道背景 = set_node_attr(ImageRect(), {'rsp_file': 'wzife.rsp',
                                            'hash_id': 3013429006,
                                            'bottom_left_x': 0,
                                            'bottom_left_y': self.director.window_h - 1})
        self.add_child('频道背景', 频道背景)

        表情开关 = set_node_attr(Animation8D(), {'rsp_file': 'wzife.rsp',
                                           'hash_id': 1494002331,
                                           'bottom_left_x': self.director.window_w - 380,
                                           'bottom_left_y': self.director.window_h + 24})
        表情开关.is_playing = False
        self.add_child('表情开关', 表情开关)

        btn_语音 = set_node_attr(Button(), {'rsp_file': 'other2.rsp',
                                            'hash_id': 65874,
                                            'bottom_left_x': 44,
                                            'bottom_left_y': self.director.window_h - 3})
        self.add_child('btn_语音', btn_语音)

        btn_冒泡 = set_node_attr(Button(), {'rsp_file': 'other2.rsp',
                                            'hash_id': 65875,
                                            'bottom_left_x': 62,
                                            'bottom_left_y': self.director.window_h - 3})
        self.add_child('btn_冒泡', btn_冒泡)

        # text = '#xt#R红色字体#Y黄色字体#24瞪眼瞪眼\n#P换行之后显示一行废话,废话废话废话废话废话...\n再换行之后#G绿色试试看?#12凑字数凑字数凑字数凑字数凑字数凑字数凑字数凑字数凑字数凑字数凑字数凑字数凑字数凑字数凑字数一二三四五六七八abcdefgABCDEFG'
        text = '#xt#W欢迎来到梦幻西游'
        信息流文本 = RichText(text, 400, 120)
        # 信息流文本.append_text('#dq#W[狂啸一二三] #G嘛呢兄弟?#24#P闹呢?抽你大嘴巴子信不信?再瞅一眼试试#120')
        # 信息流文本.append_text('#dq#W[狂啸一二三] #Y26W无限收C66,有的++++++++++++#43')
        # 信息流文本.append_text('#dq#W[狂啸一二三] 梦幻西游,人人都玩,不玩才怪!!!')
        # 信息流文本.append_text('#dq#W[狂啸一二三] #108#R谁给我一点钱,快穷死啦#108')
        # 信息流文本.append_text('#dq#W[狂啸一二三] #G今天副本不会又要空车吧...淦#60')
        信息流文本.x, 信息流文本.y = 8, 8
        self.child('聊天区背景').add_child('信息流文本', 信息流文本)

        消息输入 = LineEdit('', 326, font_size=15)
        消息输入.is_active = False
        消息输入.x, 消息输入.y = 87, self.director.window_h - 21
        self.add_child('消息输入框', 消息输入)
        消息输入.setup()

        # 消息输入2 = TextEdit('', 200, 200, font_size=16)
        # 消息输入2.is_active = False
        # 消息输入2.x, 消息输入2.y = 200, 200
        # self.add_child('消息输入框2', 消息输入2)

    def check_event(self):
        super(MessageArea, self).check_event()
        if self.child('表情开关').rect.collidepoint(pygame.mouse.get_pos()):
            self.child('表情开关').is_playing = True
            if self.director.match_mouse_event(STOP, MOUSE_LEFT_DOWN):
                emoji_window = self.director.get_node('function_layer/emoji_window')
                emoji_window.visible = not emoji_window.visible
        else:
            self.child('表情开关').is_playing = False
            self.child('表情开关').cur_animation.frame_index = 0

        if self.child('消息输入框').enter_event:
            text = self.child('消息输入框').text
            if text:
                ch = '当前'
                send(C_角色发言, dict(频道=ch, 内容=text))
                self.child('消息输入框').clear_text()

    def update(self):
        pass
