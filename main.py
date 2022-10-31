from Node.director import game_director
from Nt.nt_item import ConfigItem
from Common.common import *
from UiLayer.FunctionLayer.function_layer import FunctionLayer
from UiLayer.WindowLayer.window_layer import WindowLayer, Window
from Node.button import ButtonClassicRed
from Node.image_rect import ImageRect
from Node.text_edit import TextEdit
from Game.res_manager import fill_res
from UiLayer.WindowLayer.hero_attr import HeroAttr
from UiLayer.WindowLayer.hero_skill import HeroSkill
from Node.prompt import GamePrompt, GamePromptManager

pygame.display.set_caption("梦幻西游ONLINE - pygame")
icon = pygame.image.load('my.ico')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
director = game_director
director.setup_from_config('game_ui.conf')
director.add_child('gp_manager', GamePromptManager())
print_node(director)

world = director.get_node('scene/world_scene')
world.change_map(1092)
camera = director.get_node('scene/world_scene/camera')

hero = world.get_node('hero')
hero.setup()
hero.x, hero.y = 300, 300

fl = FunctionLayer()
director.add_child('function_layer', fl)

wl = WindowLayer()
director.add_child('window_layer', wl)
wl.is_hover_enabled = False

win = HeroAttr()
win.visible = False
wl.add_child('人物属性', win)

win2 = HeroSkill()
win2.visible = False
wl.add_child('人物技能', win2)

# pt = GamePrompt('#24一锄头下去竟挖塌了妖怪的巢穴, 无数妖怪宝宝正在#R北俱芦洲#Y捣乱, 快去收服他们吧!')
# pt.setup()
# wl.add_child('pt', pt)


while True:
    director.event_handler.update()
    director.update()
    traverse_node(director)
    traverse_node_reverse(director)

    pygame.display.flip()
    clock.tick(director.game_fps)

