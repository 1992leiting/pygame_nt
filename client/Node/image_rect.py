import pygame.image
from Node.node import Node


class ImageRect(Node):
    def __init__(self, with_mask=False):
        super(ImageRect, self).__init__()
        self.ori_image = None  # 原始的素材image, 未裁切
        self.image = None  # pygame.image
        self.raw_image = None  # 没有裁切过的
        self.kx, self.ky = 0, 0
        self.width, self.height = 0, 0
        self.disp_image = None  # 当前显示的image
        self.outline_points = []
        self.mask_outline = {'outline': [], 'color': (255, 255, 255), 'width': 3}
        self.is_hover_enabled = False
        self.rsp_file = ''
        self.hash_id = 0
        self.modulation = None
        if with_mask:
            # 添加一个mask层, 实现遮罩效果
            node = ImageRect().from_color((0, 0, 0, 0))
            node.is_hover_enabled = False
            self.add_child('mask', node)

    def setup(self):
        if self.rsp_file and self.hash_id:
            from Game.res_manager import fill_image_rect
            fill_image_rect(self, self.rsp_file, self.hash_id)

    def setup_outline(self, color=(255, 255, 255), width=1, threshold=10):
        mask = pygame.mask.from_surface(self.image, threshold=10)
        self.mask_outline['color'] = color
        self.mask_outline['width'] = width
        self.mask_outline['outline'] = mask.outline()
        self.outline_points = mask.outline()
        for i, point in enumerate(self.mask_outline['outline']):
            self.mask_outline['outline'][i] = (point[0] + self.x, point[1] + self.y)

    def from_img_file(self, file):
        self.image = pygame.image.load(file)
        self.raw_image = self.image.copy()
        self.width, self.height = self.image.get_size()
        return self

    def from_color(self, color):
        """
        通过RGBA创建
        :param color: (r, g, b, a)
        :return:
        """
        self.image = pygame.Surface((self.director.window_w, self.director.window_h), flags=pygame.SRCALPHA)
        self.raw_image = self.image.copy()
        self.image.fill(color)
        return self

    def crop(self, x, y, width, height):
        from Common.common import crop_image
        self.disp_image = crop_image(self.raw_image, x, y, width, height)
        self.width, self.height = width, height

    def auto_sizing(self, w=0, h=0, margin=0):
        self.disp_image = None
        if w == 0:
            w = self.width
        if h == 0:
            h = self.height
        from Common.common import auto_sizing
        self.image = auto_sizing(self.raw_image, w, h, margin)
        self.width, self.height = w, h

    def set_modulation(self, rgba):
        mask = self.child('mask')
        print('img mudl:', rgba, mask)
        if mask:
            mask.auto_sizing(self.width, self.height)
            mask.image.fill(rgba)
            self.modulation = rgba

    def reset_modulation(self):
        if self.modulation:
            mask = self.child('mask')
            mask.fill((0, 0, 0, 0))
            self.modulation = None

    def draw(self):
        if not self.disp_image:
            self.disp_image = self.image
        if self.disp_image and not self.disp_image.get_locked():
            self.director.screen.blit(self.disp_image, (self.x - self.kx, self.y - self.ky))

            if len(self.mask_outline['outline']) > 2:
                for i, point in enumerate(self.outline_points):
                    self.mask_outline['outline'][i] = (point[0] + self.x, point[1] + self.y)
                pygame.draw.polygon(self.director.screen, self.mask_outline['color'], self.mask_outline['outline'], self.mask_outline['width'])

