from Node.node import Node


class Camera(Node):
    def __init__(self):
        super(Camera, self).__init__()
        self.width, self.height = self.director.WINDOW_W, self.director.WINDOW_H
        self.binding_node = None
        self.limit = [0, 0, 999999, 999999]

    @property
    def center_x(self):
        return self.x + self.width / 2

    @center_x.setter
    def center_x(self, cx):
        self.x = cx - self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    @center_y.setter
    def center_y(self, cy):
        self.y = cy - self.height / 2

    def move(self, dx, dy):
        # print('camera move:', dx, dy)
        self.center_x += dx
        self.center_y += dy

    def move_to(self, xx, yy):
        self.center_x, self.center_y = xx, yy

    def update(self):
        # self.x, self.y最终转换为绑定节点的坐标变化, camera自身并不显示内容
        self.x = max(self.x, self.limit[0])
        self.x = min(self.x, self.limit[2])
        self.y = max(self.y, self.limit[1])
        self.y = min(self.y, self.limit[3])

        if self.binding_node:
            self.binding_node.x = -self.x
            self.binding_node.y = -self.y
