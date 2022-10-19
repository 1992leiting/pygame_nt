import pygame
from Node.node import Node
# from PIL import Image


class ProgressBar(Node):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self._progress = 100
        self.image = None
        self.disp_image = None  # 当前显示的image

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, p):
        self._progress = p
        self.setup()

    def set_ratio(self, a, b):
        """
        通过比例设置进度值
        :param a: 当前值
        :param b: 最大值
        :return:
        """
        self._progress = int(a * 100 / b)
        self.setup()

    def setup(self):
        """
        进行横向裁切
        :return:
        """
        # if self.image:
        #     img_bytes = self.image.get_buffer()
        #     w = int(self.width * self.progress / 100)
        #     crop_box = (0, 0, w, self.height)
        #     pil_img = Image.frombuffer('RGBA', (self.width, self.height), img_bytes).crop(crop_box)
        #     img_bytes = pil_img.tobytes()
        #     self.image = pygame.image.fromstring(img_bytes, (w, self.height), 'RGBA')
        if self.image:
            from common import crop_image
            w = int(self.width * self.progress / 100)
            self.disp_image = crop_image(self.image, 0, 0, w, self.height)

    def draw(self):
        if not self.disp_image:
            self.disp_image = self.image
        if self.disp_image:
            self.director.SCREEN.blit(self.disp_image, (self.x - self.kx, self.y - self.ky))
