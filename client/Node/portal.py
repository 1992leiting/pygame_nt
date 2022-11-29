import pygame.draw
from Node.animation import Animation8D
from Common.socket_id import *
from Common.constants import *


class Portal(Animation8D):
    def __init__(self):
        from Game.res_manager import fill_animation8d
        super(Portal, self).__init__()
        fill_animation8d(self, 'mapani.rsp', 2135735436)
        self.portal_id = 0
        self._rect = pygame.Rect(0, 0, 0, 0)

    def update(self):
        # 减小传送阵rect范围, 主角走到传送阵上才触发传送
        self._rect = self.cur_animation.rect
        self._rect.x += 20
        self._rect.y += 10
        self._rect.width -= 40
        self._rect.height -= 20
        # pygame.draw.rect(self.director.screen, (255, 255, 255), self._rect, 2)

        hero = game.hero
        hero_pos = (hero.x, hero.y)
        if self._rect.collidepoint(hero_pos):
            if self.director.is_hero_in_portal == 0 and hero.is_moving:
                hero.set_path([])
                print('触发传送:', self.portal_id)
                send_data = {'portal_id': self.portal_id}
                self.director.client.send(C_传送点传送, send_data)
            self.director.is_hero_in_portal = self.portal_id
        else:
            if self.director.is_hero_in_portal == self.portal_id:
                self.director.is_hero_in_portal = 0
