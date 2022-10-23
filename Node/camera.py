from Node.node import Node


class Camera(Node):
    def __init__(self):
        super(Camera, self).__init__()
        self.binding_node = None
        self.limit = [0, 0, 999999, 999999]

    @property
    def center_x(self):
        return self.x + self.director.window_w / 2

    @center_x.setter
    def center_x(self, cx):
        self.x = cx - self.director.window_w / 2

    @property
    def center_y(self):
        return self.y + self.director.window_h / 2

    @center_y.setter
    def center_y(self, cy):
        self.y = cy - self.director.window_h / 2

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

        # camera本质控制的是父节点的移动, camera偏移多少, 父节点就反方向偏移
        if self._parent:
            self._parent.x = -self.x
            self._parent.y = -self.y
