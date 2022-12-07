import pygame

from Node.node import Node
from Common.constants import *


class GameScene(Node):
    def __init__(self):
        super(GameScene, self).__init__()

    def check_event(self):
        super(GameScene, self).check_event()
        if game.director.match_kb_event(STOP, pygame.K_F5):
            game.director.change_scene(BATTLE_SCENE)
