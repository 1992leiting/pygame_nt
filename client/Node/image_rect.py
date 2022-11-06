import pygame.image
from Node.node import Node


class ImageRect(Node):
    def __init__(self):
        super(ImageRect, self).__init__()
        self.ori_image = None  # 原始的素材image, 未裁切
        self.image = None  # pygame.image
        self.kx, self.ky = 0, 0
        self.width, self.height = 0, 0
        self.disp_image = None  # 当前显示的image
        self.mask_outline = {'outline': [], 'color': (255, 255, 255), 'width': 1}
        self.is_hover_enabled = False
        self.rsp_file = ''
        self.hash_id = 0

    def setup(self):
        if self.rsp_file and self.hash_id:
            from Game.res_manager import fill_image_rect
            fill_image_rect(self, self.rsp_file, self.hash_id)

    def setup_outline(self, color=(255, 255, 255), width=1, threshold=10):
        mask = pygame.mask.from_surface(self.image, threshold=10)
        self.mask_outline['color'] = color
        self.mask_outline['width'] = width
        self.mask_outline['outline'] = mask.outline()
        for i, point in enumerate(self.mask_outline['outline']):
            self.mask_outline['outline'][i] = (point[0] + self.x, point[1] + self.y)

    def from_img_file(self, file):
        self.image = pygame.image.load(file)
        self.width, self.height = self.image.get_size()
        return self

    def from_color(self, color):
        """
        通过RGBA创建
        :param color: (r, g, b, a)
        :return:
        """
        self.image = pygame.Surface((self.director.window_w, self.director.window_h), flags=pygame.SRCALPHA)
        self.image.fill(color)
        return self

    def crop(self, x, y, width, height):
        from Common.common import crop_image
        self.disp_image = crop_image(self.image, x, y, width, height)
        self.width, self.height = width, height

    def auto_sizing(self, w=0, h=0, margin=0):
        if w == 0:
            w = self.width
        if h == 0:
            h = self.height
        # print('image auto size:', w, h)
        from Common.common import auto_sizing
        self.image = auto_sizing(self.image, w, h, margin)
        self.width, self.height = w, h

    def draw(self):
        if not self.disp_image:
            self.disp_image = self.image
        if self.disp_image and not self.disp_image.get_locked():
            self.director.screen.blit(self.disp_image, (self.x - self.kx, self.y - self.ky))

            if len(self.mask_outline['outline']) > 2:
                pygame.draw.polygon(self.director.screen, self.mask_outline['color'], self.mask_outline['outline'], self.mask_outline['width'])
