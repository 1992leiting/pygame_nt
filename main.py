from Node.director import game_director
from Nt.nt_item import ConfigItem
from Common.common import *
from UiLayer.FunctionLayer.function_layer import FunctionLayer
from UiLayer.WindowLayer.window_layer import WindowLayer, Window

pygame.display.set_caption("梦幻西游ONLINE - pygame")
icon = pygame.image.load('my.ico')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
director = game_director
director.setup_from_config('game_ui.conf')
print_node(director)

world = director.get_node('scene/world_scene')
world.change_map(1092)
camera = director.get_node('scene/world_scene/camera')

hero = world.get_node('hero')
hero.setup()
hero.x, hero.y = 300, 300

fl = FunctionLayer()
director.add_child('function_layer', fl)
fl.setup()

wl = WindowLayer()
director.add_child('window_layer', wl)

win = Window()
director.add_child('win', win)
win.setup()

while True:
    director.event_handler.update()
    director.update()
    traverse_node(director)
    traverse_node_reverse(director)

    pygame.display.flip()
    clock.tick(director.game_fps)

