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
from UiLayer.WindowLayer.smap import Smap
from UiLayer.WindowLayer.hero_bag import HeroBag

pygame.display.set_caption("梦幻西游ONLINE - pygame")
icon = pygame.image.load('my.ico')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
game.director = game_director
# director.setup_from_config('game_ui.conf')
game.director.add_child('gp_manager', PromptManager())
print_node(game.director)

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

win2 = Smap()
win2.enable = False
wl.add_child('小地图', win2)

win2 = HeroBag()
win2.enable = False
wl.add_child('道具行囊', win2)


while True:

    game.director.screen.fill((0, 0, 0))
    game.director.event_handler.update()
    game.director.update()
    traverse_node(game.director)
    traverse_node_reverse(game.director)

    pygame.display.flip()
    clock.tick(game.director.game_fps)



