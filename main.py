import pygame.time

from Node.node import Node
from Node.director import Director
from Nt.nt_item import ConfigItem
from Common.common import *

pygame.display.set_caption("梦幻西游ONLINE - pygame")
icon = pygame.image.load('my.ico')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
director = Director()
director.setup_from_config('game_ui.conf')
print_node(director)

world = director.get_node('scene/world_scene')
world.change_map(1501)

while True:
    director.event_handler.update()
    traverse_node(director)
    traverse_node_reverse(director)

    pygame.display.flip()
    clock.tick(director.game_fps)

