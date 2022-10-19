import pygame.draw
from Node.animation import Animation8D


class Portal(Animation8D):
    def __init__(self):
        from res_manager import fill_animation8d
        super(Portal, self).__init__()
        fill_animation8d(self, 'mapani.rsp', 2135735436)
        self.portal_id = 0
        self._rect = pygame.Rect(0, 0, 0, 0)

    def update(self):
        self.cur_animation = self.child('0')
        # 减小传送阵rect范围, 主角走到传送阵上才触发传送
        self._rect = self.cur_animation.rect
        self._rect.x += 30
        self._rect.y += 15
        self._rect.width -= 60
        self._rect.height -= 30
        # pygame.draw.rect(self.director.SCREEN, (255, 255, 255), self._rect, 2)

        hero = self.director.root.child('world').child('hero')
        hero_pos = (hero.x, hero.y)
        if self._rect.collidepoint(hero_pos):
            if self.director.HERO_IN_PORTAL == 0:
                print('触发传送:', self.portal_id)
                send_data = {'传送阵id': self.portal_id}
                self.director.client.send('触发传送阵', send_data)
            self.director.HERO_IN_PORTAL = self.portal_id
        else:
            if self.director.HERO_IN_PORTAL == self.portal_id:
                self.director.HERO_IN_PORTAL = 0
