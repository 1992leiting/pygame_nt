from Node.node import Node


class HeroAttributes(Node):
    def __init__(self):
        super(HeroAttributes, self).__init__()
        self.director.child('window_layer').append(self)
        self.width, self.height = 294, 412
        self.x, self.y = self.director.window_w - self.width - 1, self.director.window_h / 2 - self.height // 2
        self.visible = False
