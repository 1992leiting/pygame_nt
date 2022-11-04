from Node.node import Node
from UiLayer.FunctionLayer.button_area import ButtonArea
from UiLayer.FunctionLayer.statusbar_area import StatusbarArea
from UiLayer.FunctionLayer.time_area import TimeArea
from UiLayer.FunctionLayer.message_area import MessageArea
from UiLayer.FunctionLayer.emoji_window import EmojiWindow


class FunctionLayer(Node):
    def __init__(self):
        super(FunctionLayer, self).__init__()

        button_area = ButtonArea()
        self.add_child('button_area', button_area)
        statusbar_area = StatusbarArea()
        self.add_child('statusbar_area', statusbar_area)
        time_area = TimeArea()
        self.add_child('time_area', time_area)
        message_area = MessageArea()
        self.add_child('message_area', message_area)
        emoji_window = EmojiWindow()
        emoji_window.visible = False
        self.add_child('emoji_window', emoji_window)
