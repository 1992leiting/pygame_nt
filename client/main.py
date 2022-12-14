import time

from Node.director import game_director
from Common.common import *
from UiLayer.FunctionLayer.function_layer import FunctionLayer
from UiLayer.WindowLayer.window_layer import WindowLayer, Window
from Node.button import ButtonClassicRed
from Node.image_rect import ImageRect
from Node.label import Label
from Node.text_edit import TextEdit
from Node.rich_text import RichText
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
from UiLayer.WindowLayer.battle_skill import BattleSkill
from Node.scrollbar import Scrollbar
from Node.list_view import *

pygame.display.set_caption("梦幻西游ONLINE - pygame")
icon = pygame.image.load('my.ico')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
game.director = game_director
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

win2 = BattleSkill()
win2.enable = False
wl.add_child('战斗技能栏', win2)

# 滚动条测试
# sb = Scrollbar()
# sb.x, sb.y = 100, 100
# sb.setup()
# game.director.add_child('test_sb', sb)

# ListView测试
lv = ListView()
lv.x, lv.y = 10, 10
# li = ListItem()
li = Label(text='测试item1')
lv.add_child('1', li)
# li = ListItem()
li = Label(text='测试item2\n22222')
lv.add_child('2', li)
game.director.add_child('lv', lv)


while True:
    # print('main...')
    game.director.screen.fill((0, 0, 0))
    game.director.event_handler.update()
    game.director.update()
    traverse_node(game.director)
    traverse_node_reverse(game.director)

    pygame.display.flip()
    clock.tick(game.director.game_fps)



