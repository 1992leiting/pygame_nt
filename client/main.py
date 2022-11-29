import time

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
from UiLayer.WindowLayer.simple_login import SimpleLogin
from Node.prompt import GamePrompt, PromptManager
from Common.constants import game
from UiLayer.WindowLayer.simple_register import SimpleRegister
from UiLayer.WindowLayer.simple_hero_select import SimpleHeroSelect
from UiLayer.WindowLayer.simple_create_player import SimpleCreatePlayer
from UiLayer.WindowLayer.dialog import Dialog

pygame.display.set_caption("梦幻西游ONLINE - pygame")
icon = pygame.image.load('my.ico')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
game.director = game_director
# director.setup_from_config('game_ui.conf')
game.director.add_child('gp_manager', PromptManager())
print_node(game.director)

# world = director.get_node('scene/world_scene')
# world.change_map(1092)
# camera = director.get_node('scene/world_scene/camera')
#
# hero = world.get_node('hero')
# hero.setup()
# hero.x, hero.y = 300, 300
#
# fl = FunctionLayer()
# director.add_child('function_layer', fl)
#
wl = WindowLayer()
game.director.add_child('window_layer', wl)
game.window_layer = wl

win = SimpleLogin()
wl.add_child('简易登陆', win)
win.enable = True

win = SimpleRegister()
wl.add_child('简易注册', win)
win.enable = False

win = SimpleHeroSelect()
wl.add_child('简易选择角色', win)
win.enable = False

win = SimpleCreatePlayer()
wl.add_child('简易创建角色', win)
win.enable = False

#
win = HeroAttr()
win.enable = False
wl.add_child('人物属性', win)

win2 = HeroSkill()
win2.enable = False
wl.add_child('人物技能', win2)

win2 = Dialog()
win2.enable = False
wl.add_child('对话栏', win2)


while True:
    # print('---------')
    # t = time.time()
    game.director.screen.fill((0, 0, 0))
    game.director.event_handler.update()
    # t1 = time.time()
    game.director.update()
    # t2 = time.time()
    traverse_node(game.director)
    # t3 = time.time()
    traverse_node_reverse(game.director)
    # t4 = time.time()
    # print(int((t1 - t)*1000), int((t2 - t1)*1000), int((t3 - t2)*1000), int((t4 - t3)*1000))

    pygame.display.flip()
    clock.tick(game.director.game_fps)

