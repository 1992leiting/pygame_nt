from Node.node import Node


class Director(Node):
    def __init__(self):
        super(Director, self).__init__()
        self.screen = None
