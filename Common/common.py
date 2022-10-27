import os.path
import sys
import math
import tkinter
import tkinter.messagebox as mb
import time
import pygame
from Node.node import Node
from Nt.nt_item import ConfigItem
import csv


def read_csv(file):
    result = []
    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)

    return result


def new_node(node_type, *args):
    if node_type == 'Node':
        from Node.node import Node
        return Node()
    elif node_type == 'Animation':
        from Node.animation import Animation
        return Animation()
    elif node_type == 'Animation8D':
        from Node.animation import Animation8D
        return Animation8D()
    elif node_type == 'Button':
        from Node.button import Button
        return Button()
    elif node_type == 'ImageRect':
        from Node.image_rect import ImageRect
        return ImageRect()
    elif node_type == 'Label':
        from Node.label import Label
        return Label()
    elif node_type == 'ProgressBar':
        from Node.progressbar import ProgressBar
        return ProgressBar()
    elif node_type == 'RichText':
        from Node.rich_text import RichText
        return RichText()
    elif node_type == 'TextEdit':
        from Node.text_edit import TextEdit
        return TextEdit()
    elif node_type == 'LineEdit':
        from Node.text_edit import LineEdit
        return LineEdit()
    elif node_type == 'Camera':
        from Node.camera import Camera
        return Camera()
    elif node_type == 'BasicCharacter':
        from Node.character import BasicCharacter
        return BasicCharacter
    elif node_type == 'Character':
        from Node.character import Character
        return Character()
    elif node_type == 'NPC':
        from Node.character import NPC
        return NPC
    elif node_type == 'BattleUnit':
        from Node.character import BattleUnit
        return BattleUnit()
    elif node_type == 'Emoji':
        from Node.emoji import Emoji
        return Emoji()
    elif node_type == 'HpEffect':
        from Node.hp_effect import HpEffect
        return HpEffect
    elif node_type == 'BuffEffect':
        from Node.magic_effect import BuffEffect
        return BuffEffect(args)
    elif node_type == 'FullScreenEffect':
        from Node.magic_effect import FullScreenEffect
        return FullScreenEffect(args)
    elif node_type == 'MapMask':
        from Node.map_mask import MapMask
        return MapMask()
    elif node_type == 'Portal':
        from Node.portal import Portal
        return Portal()
    elif node_type == 'World':
        from Node.world import World
        return World()
    elif node_type == 'Director':
        from Node.director import Director
        return Director()
    elif node_type == 'Mouse':
        from Node.mouse import Mouse
        return Mouse()
    elif node_type == 'ButtonClassicRed':
        from Node.button import ButtonClassicRed
        return ButtonClassicRed()
    else:
        raise KeyError('未知节点类型:{}'.format(node_type))


def traverse_config_item(config_item: ConfigItem, node: Node):
    node.node_name = config_item.node_name
    node.uuid = config_item.node_uuid
    if config_item.children:
        for name, child_config_item in config_item.children.items():
            child_node = new_node(child_config_item.node_type)
            child_node.node_name = child_config_item.node_name
            child_node.uuid = child_config_item.node_uuid
            node.add_child(child_config_item.node_name, child_node)
            traverse_config_item(child_config_item, child_node)


def traverse_node(node):
    """
    递归函数, 依次update节点及其所有子节点
  :      param node:
  :      return:
    """
    # 先复制所有children, 因为刷新过程中, children可能会变化, 这时候继续遍历会抛出异常
    children = node.get_children().copy()
    # mouse节点挪到末端, 总是显示在UI最上层
    if 'mouse' in children:
        m = children['mouse']
        del children['mouse']
        children['mouse'] = m

    if len(children) > 0:
        # 遍历所有子节点并绘制
        for child in children.values():
            if not child.enable:
                break
            child.update()
            if child.visible:
                child.draw()
                if child.ysort:
                    child.process_ysort()
            traverse_node(child)


def traverse_node_reverse(node):
    """
    递归函数, 反序依次update节点及其所有子节点
  :      param node:
  :      return:
    """
    # 先复制所有children, 因为刷新过程中, children可能会变化, 这时候继续遍历会抛出异常
    children = node.get_children().copy()
    if len(children) > 0:
        values = list(children.values())
        values.reverse()
        for child in values:
            traverse_node_reverse(child)
            if child.enable and child.visible:
                if child.is_hover_enabled:
                    child.check_hover()
                child.check_event()
            else:
                continue
            # traverse_node_reverse(child)


def print_node(node):
    """
    递归函数, 打印node的结构
  :      param node:
  :      return:
    """
    if node.get_children_count() > 0:
        for child in node.get_children().values():
            s = ''.join(' - ' for _ in range(child.level)) + child.node_name  # + '[{}]'.format(type(child))
            print(s)
            print_node(child)


def calc_direction(pos, des):
    # 0↘ 1↙ 2↖ 3↗ 4↓ 5← 6↑ 7→
    # 计算两点之间的夹角, rad为弧度, angle为角度
    rad = math.atan2(-des[1] - (-pos[1]), des[0] - pos[0])
    angle = math.degrees(rad)

    # print('cal dir:', pos, des, angle)
    if -112.5 < angle <= -67.5:
        return 4  # 6
    elif -67.5 < angle <= -22.5:
        return 0  # 3
    elif -22.5 < angle <= 22.5:
        return 7
    elif 22.5 < angle <= 67.5:
        return 3  # 0
    elif 67.5 < angle <= 112.5:
        return 6  # 4
    elif 112.5 < angle <= 157.5:
        return 2  # 1
    elif angle > 157.5 or angle <= -157.5:
        return 5
    else:
        return 1  # 2


def update_timer(timer, interval):
    """
    用于判断timer是否超过间隔值, 如果是则重新赋值最新的时间戳
  :      param timer:
  :      param interval:
  :      return:
    """
    if time.time() - timer > interval:
        timer = time.time()
        return True
    else:
        return False


def set_node_attr(node, attrs: dict):
    """
    批量设置节点参数
  :      param node: 节点对象
  :      param attrs: dict类型, 键为参数名称, 值为参数数值
  :      return: 节点对象
    """
    from Game.res_manager import fill_res
    if 'rsp_file' in attrs and 'hash_id' in attrs:
        fill_res(node, attrs['rsp_file'], attrs['hash_id'])
    for k, v in attrs.items():
        if hasattr(node, k):
            setattr(node, k, v)
    return node


def show_error(text, tp='错误'):
    top = tkinter.Tk()
    top.geometry('0x0+999999+0')
    try:
        mb.showerror(tp, text)
    except:
        pass


def exit_game():
    pygame.quit()
    sys.exit()


def game_start(gl):
    print('game start...')
    from Node.character import Character
    from Node.world import World
    from Node.camera import Camera
    from UiLayer.FunctionLayer.function_layer import FunctionLayer
    from UiLayer.WindowLayer.window_layer import WindowLayer

    GL = gl
    # 英雄节点
    char = Character()
    char.type = 'hero'
    char.set_data(GL.HERO_DATA)

    # 镜头节点
    camera = Camera()
    GL.root.add_child('camera', camera)

    # world节点
    world = World()
    world.ysort = True
    GL.root.add_child('world', world)
    world.add_child('hero', char)
    GL.root.child('world').change_map(int(GL.HERO_DATA['地图数据']['编号']))
    camera.binding_node = world

    # FunctionLayer
    function_layer = FunctionLayer()
    GL.root.add_child('function_layer', function_layer)

    # WindowLayer
    window_layer = WindowLayer()
    GL.root.add_child('window_layer', window_layer)

    GL.STARTED = True
    GL.client.send('进入游戏', {})


def crop_image(image: pygame.image, x, y, w, h):
    # from PIL import Image
    # img_bytes = image.get_buffer()
    # crop_box = (x, y, w, h)
    # pil_img = Image.frombuffer('RGBA', (image.get_width(), image.get_height()), img_bytes).crop(crop_box)
    # img_bytes = pil_img.tobytes()
    # out_image = pygame.image.fromstring(img_bytes, (w, h), 'RGBA')

    out_image = image.subsurface(pygame.Rect(x, y, w, h))
    return out_image


def auto_sizing(image: pygame.image, width, height, margin=0):
    w, h = image.get_size()  # 原始尺寸
    if width > w or height > h:
        return image
    surf = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    # 左上角
    x, y, ww, hh = 0, 0, width/2, height/2
    sub_img = image.subsurface(pygame.Rect(x, y, ww, hh))
    surf.blit(sub_img, (0, 0))
    # 右上角
    x, y, ww, hh = w - width/2, 0, width/2, height/2
    sub_img = image.subsurface(pygame.Rect(x, y, ww, hh))
    surf.blit(sub_img, (width / 2, 0))
    # 左下角
    x, y, ww, hh = 0, h - height / 2 + margin, width / 2, height / 2 - margin
    sub_img = image.subsurface(pygame.Rect(x, y, ww, hh))
    surf.blit(sub_img, (0, height / 2))
    # 右下角
    x, y, ww, hh = w - width/2, h - height/2 + margin, width/2, height/2 - margin
    sub_img = image.subsurface(pygame.Rect(x, y, ww, hh))
    surf.blit(sub_img, (width / 2, height/2))
    return surf


def get_color(name: str):
    from Common.constants import colors, MY_COLOR
    if name in MY_COLOR:
        name = MY_COLOR[name]
    if name not in colors:
        return 255, 255, 255
    r = int(colors[name]['R'])
    g = int(colors[name]['G'])
    b = int(colors[name]['B'])
    return r, g, b


def int2hex(num: int):
    """
    将10进制数字转换成16进制并去除0x, 保留8位(不足补0)
    e.g. 1234533 --> '0012D665'
  :      param num:
  :      return:
    """
    s = hex(num).lstrip('0x').upper().zfill(8)
    return s


def set_bgm_volume(val: float):
    if val < 0:
        val = 0
    if val > 1.0:
        val = 1.0
    pygame.mixer.music.set_volume(val)


def play_scene_bgm(mapid: int):
    """
    播放场景地图的背景音乐
  :      param mapid: 地图id
  :      return:
    """
    from Common.constants import music_dir
    file = music_dir + str(mapid) + '.mp3'
    if not os.path.exists(file):
        print('BGM文件丢失:', file)
        return
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=200)


def play_battle_music(name):
    from Common.constants import music_dir
    file = music_dir + name + '.mp3'
    if not os.path.exists(file):
        print('BGM文件丢失:', file)
        return
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=200)


def play_skill_effect_sound(name):
    from Database.sound_res import get_sound
    res = get_sound(name)
    if res:
        folder = res['资源'].replace('.dll', '')
        file = res['文件源']
        path = constants.sound_dir + folder + '/' + int2hex(file) + '.ogg'
        if os.path.exists(path):
            sd = pygame.mixer.Sound(path)
            sd.play()
        else:
            print('技能/特效音源文件丢失:', path)
    else:
        print('技能/特效音源未找到:', name)


def play_char_sound(char, action):
    from Database.sound_res import get_sound
    res = get_sound(char)
    if res:
        if action in res:
            folder = res['资源'].replace('.dll', '')
            file = res[action]
            path = constants.sound_dir + folder + '/' + int2hex(file) + '.ogg'
            if os.path.exists(path):
                sd = pygame.mixer.Sound(path)
                sd.play()
            else:
                print('技能/特效音源文件丢失:', path)
        else:
            print('model音效未找到:', char, action)
    else:
        print('model音效未找到:', char, action)


def get_weapon_type(w_name):
    if w_name in ["红缨枪", "曲尖枪", "锯齿矛", "乌金三叉戟", "火焰枪", "墨杆金钩", "玄铁矛", "金蛇信", "丈八点钢矛", "暗夜", "梨花", "霹雳", "刑天之逆", "五虎断魂", "飞龙在天", "天龙破城", "弑皇"]:
        return '枪矛'
    if w_name in ["青铜斧", "开山斧", "双面斧", "双弦钺", "精钢禅钺", "黄金钺", "乌金鬼头镰", "狂魔镰", "恶龙之齿", "破魄", "肃魂", "无敌", "五丁开山", "元神禁锢", "护法灭魔", "碧血干戚", "裂天"]:
        return '斧钺'
    if w_name in ["青铜短剑", "铁齿剑", "吴越剑", "青锋剑", "龙泉剑", "黄金剑", "游龙剑", "北斗七星剑", "碧玉剑", "鱼肠", "倚天", "湛卢", "魏武青虹", "灵犀神剑", "四法青云", "霜冷九州", "擒龙"]:
        return '剑'
    if w_name in ["双短剑", "镔铁双剑", "龙凤双剑", "竹节双剑", "狼牙双剑", "鱼骨双剑", "赤焰双剑", "墨玉双剑", "梅花双剑", "阴阳", "月光双剑", "灵蛇", "金龙双剪", "连理双树", "祖龙对剑", "紫电青霜", "浮犀"]:
        return '双短剑'
    if w_name in ["五色缎带", "幻彩银纱", "金丝彩带", "无极丝", "天蚕丝带", "云龙绸带", "七彩罗刹", "缚神绫", "九天仙绫", "彩虹", "流云", "碧波", "秋水落霞", "晃金仙绳", "此最相思", "揽月摘星", "九霄"]:
        return '飘带'
    if w_name in ["铁爪", "天狼爪", "幽冥鬼爪", "青龙牙", "勾魂爪", "玄冰刺", "青刚刺", "华光刺", "龙鳞刺", "撕天", "毒牙", "胭脂", "九阴勾魂", "雪蚕之刺", "贵霜之牙", "忘川三途", "离钩"]:
        return '爪刺'
    if w_name in ["折扇", "铁骨扇", "精钢扇", "铁面扇", "百折扇", "劈水扇", "神火扇", "阴风扇", "风云雷电", "太极", "玉龙", "秋风", "画龙点睛", "秋水人家", "逍遥江湖", "浩气长舒", "星瀚"]:
        return '扇'
    if w_name in ["细木棒", "金丝魔棒", "玉如意", "点金棒", "云龙棒", "幽路引魂", "满天星", "水晶棒", "日月光华", "沧海", "红莲", "盘龙", "降魔玉杵", "青藤玉树", "墨玉骷髅", "丝萝乔木", "醍醐"]:
        return '魔棒'
    if w_name in ["松木锤", "镔铁锤", "八棱金瓜", "狼牙锤", "烈焰锤", "破甲战锤", "震天锤", "巨灵神锤", "天崩地裂", "八卦", "鬼牙", "雷神", "混元金锤", "九瓣莲花", "鬼王蚀日", "狂澜碎岳", "碎寂"]:
        return '锤'
    if w_name in ["牛皮鞭", "牛筋鞭", "乌龙鞭", "钢结鞭", "蛇骨鞭", "玉竹金铃", "青藤柳叶鞭", "雷鸣嗜血鞭", "混元金钩", "龙筋", "百花", "吹雪", "游龙惊鸿", "仙人指路", "血之刺藤", "牧云清歌", "霜陨"]:
        return '鞭子'
    if w_name in ["黄铜圈", "精钢日月圈", "离情环", "金刺轮", "风火圈", "赤炎环", "蛇形月", "子母双月", "斜月狼牙", "如意", "乾坤", "月光双环", "别情离恨", "金玉双环", "九天金线", "无关风月", "朝夕"]:
        return '环圈'
    if w_name in ["柳叶刀", "苗刀", "夜魔弯刀", "金背大砍刀", "雁翅刀", "破天宝刀", "狼牙刀", "龙鳞宝刀", "黑炎魔刀", "冷月", "屠龙", "血刃", "偃月青龙", "晓风残月", "斩妖泣血", "业火三灾", "鸣鸿"]:
        return '刀'
    if w_name in ["曲柳杖", "红木杖", "白椴杖", "墨铁拐", "玄铁牛角杖", "鹰眼法杖", "腾云杖", "引魂杖", "碧玺杖", "业焰", "玉辉", "鹿鸣", "庄周梦蝶", "凤翼流珠", "雪蟒霜寒", "碧海潮生", "弦月"]:
        return '法杖'
    if w_name in ["硬木弓", "铁胆弓", "紫檀弓", "宝雕长弓", "錾金宝弓", "玉腰弯弓", "连珠神弓", "游鱼戏珠", "灵犀望月", "非攻", "幽篁", "百鬼", "冥火薄天", "龙鸣寒水", "太极流光", "九霄风雷", "若木"]:
        return '弓弩'
    if w_name in ["琉璃珠", "水晶珠", "珍宝珠", "翡翠珠", "莲华珠", "夜灵珠", "如意宝珠", "沧海明珠", "无量玉璧", "离火", "飞星", "月华", "回风舞雪", "紫金葫芦", "裂云啸日", "云雷万里", "赤明"]:
        return '宝珠'
    if w_name in ["钝铁重剑", "桃印铁刃", "赭石巨剑", "壁玉长铗", "青铜古剑", "金错巨刃", "惊涛雪", "醉浮生", "沉戟天戊", "鸦九", "昆吾", "弦歌", "墨骨枯麟", "腾蛇郁刃", "秋水澄流", "百辟镇魂", "长息"]:
        return '巨剑'
    if w_name in ["素纸灯", "竹骨灯", "红灯笼", "鲤鱼灯", "芙蓉花灯", "如意宫灯", "玲珑盏", "玉兔盏", "冰心盏", "蟠龙", "云鹤", "风荷", "金风玉露", "凰火燎原", "月露清愁", "夭桃秾李", "荒尘"]:
        return '灯笼'
    if w_name in ["油纸伞", "红罗伞", "紫竹伞", "锦绣椎", "幽兰帐", "琳琅盖", "孔雀羽", "金刚伞", "落梅伞", "鬼骨", "云梦", "枕霞", "碧火琉璃", "雪羽穿云", "月影星痕", "浮生归梦", "晴雪"]:
        return '伞'
    return None


def get_model_attack_frame(model, zl=None):
    """
    模型的攻击帧, 实际攻击帧 = 动画中间帧 + 攻击帧
   :param model: 模型名称
   :param zl: 武器类型
   :return: 攻击帧: 数组,可能都有多个攻击帧(多段攻击); 累加: 多段攻击帧时击退距离是否累加(比如大力金刚攻击时击退距离累加);
    """
    攻击帧, 攻击延迟, 累加 = 2, 1.25, False
    if model == "偃无师" or model == "桃夭夭":      
        攻击帧 = -1
        攻击延迟 = 1.35
    elif model == "鬼潇潇" or model == "剑侠客" or model == "真陀护法":
        攻击帧 = 1
        攻击延迟 = 1.3
    elif model == '龙太子':
        if zl == '扇':
            攻击帧 = [-2, 5]
        if zl == '枪矛':
            攻击帧 = 1
    elif model == "玄彩娥" or model == "舞天姬" or model == "进阶毗舍童子" or model == "羊头怪" or model == "锦毛貂精":
        攻击帧 = -1
        攻击延迟 = 1.15
    elif model == "神天兵" or model == "巨魔王" or model == "杀破狼" or model == "持国巡守" or model == "雷鸟人" or model == "金饶僧" or model == "葫芦宝贝" or model == "幽灵" or model == "凤凰" or model == "野鬼" or model == "帮派妖兽" or model == "修罗傀儡鬼" or model == "踏云兽" or model == "巴蛇" or model == "黑熊":
        攻击帧 = 1
        攻击延迟 = 1.2
        if zl is not None:
            if zl == "弓弩" or zl == "弓弩1":      
                攻击延迟 = 0.88
    elif model == "虎头怪":
        if zl == '锤':
            攻击帧 = [-2, 5]
    elif model == "强盗" or model == "山贼" or model == "鼠先锋" or model == "增长巡守" or model == "灵灯侍者" or model == "般若天女" or model == "进阶雨师" or model == "进阶如意仙子" or model == "野猪精" or model == "超级玉兔" or model == "幽萤娃娃" or model == "黑熊精" or model == "蚌精" or model == "机关鸟" or model == "连弩车" or model == "蜃气妖" or model == "蛤蟆精" or model == "虾兵" or model == "蟹将" or model == "兔子怪" or model == "蜘蛛精" or model == "花妖" or model == "狐狸精" or model == "哮天犬" or model == "混沌兽" or model == "蝴蝶仙子" or model == "海毛虫" or model == "狼" or model == "老虎":
        攻击帧 = 2
        攻击延迟 = 1.12
    elif model == "机关人人形" or model == "机关兽":
        攻击帧 = 2
        攻击延迟 = 1.25
    elif model == "泡泡":
        攻击帧 = 2
        攻击延迟 = 2.1
    elif model == "混沌兽":      
        攻击延迟 = 1.35
    elif model == "狂豹人形":      
        攻击帧 = 1
        攻击延迟 = 1.4
    elif model == "海毛虫":
        攻击延迟 = 1.35
    elif model == "大海龟" or model == "骷髅怪" or model == "金身罗汉" or model == "修罗傀儡妖" or model == "曼珠沙华" or model == "幽萤娃娃":
        攻击帧 = 1
        攻击延迟 = 1.2
    elif model == "画魂" or model == "羽灵神":      
        攻击帧 = 1
        攻击延迟 = 1.1
    elif model == "天兵" or model == "巨力神猿":
        攻击帧 = 1
        攻击延迟 = 1.25
    elif model == "风伯" or model == "芙蓉仙子" or model == "毗舍童子" or model == "镜妖" or model == "千年蛇魅" or model == "小龙女":
        攻击帧 = 0
        攻击延迟 = 1.25
    elif model == "地狱战神":
        攻击帧 = [0, 9]
    elif model == "芙蓉仙子":
        攻击帧 = 0
        攻击延迟 = 1.1
    elif model == "百足将军" or model == "天将" or model == "小龙女" or model == "碧水夜叉" or model == "马面" or model == "灵鹤":
        攻击帧 = 3
        攻击延迟 = 1.23
    elif model == "鬼将":
        攻击帧 = 4
        攻击延迟 = 1.3
    elif model == '大力金刚':
        攻击帧 = [0, 5]
        累加 = True
    elif model == "赌徒":
        攻击帧 = 4
        攻击延迟 = 1.1
    elif model == "牛妖":      
        攻击帧 = 3
        攻击延迟 = 1.26
    elif model == "古代瑞兽":      
        攻击帧 = 4
        攻击延迟 = 1.2
    elif model == "知了王":
        攻击帧 = 6
        攻击延迟 = 1.32
    elif model == "黑山老妖" or model == "炎魔神":
        攻击帧 = 6
        攻击延迟 = 1.2
    elif model == "长眉灵猴":      
        攻击帧 = -1
        攻击延迟 = 1.23
    elif model == "骨精灵" or model == "狐美人" or model == "剑侠客" or model == "逍遥生" or model == "巫蛮儿" or model == "英女侠" or model == "飞燕女":
        if zl is not None:
            if zl == "魔棒":      
                攻击帧 = -1
            elif zl == "宝珠":
                攻击帧 = 2
            elif model == "英女侠":      
                攻击帧 = 0
            elif model == "飞燕女" and zl == "双短剑":      
                攻击帧 = [0, 6]
                # 累加 = True
            elif model == "飞燕女" and zl == "环圈":      
                攻击帧 = 5
            elif model == "逍遥生" and (zl == "扇"):      
                攻击帧 = 0
            elif model == "逍遥生" and (zl == "剑"):      
                攻击帧 = -1
            elif model == "巫蛮儿" and (zl == "法杖"):      
                攻击帧 = 0
            elif model == "狐美人" and zl == "爪刺":
                攻击帧 = 0
            elif model == "狐美人" and zl == "鞭":
                攻击帧 = 0
        else:
            攻击帧 = 1
        攻击延迟 = 1.25

    if type(攻击帧) == int:
        攻击帧 = [攻击帧, 攻击帧+2]

    return 攻击帧, 累加, 攻击延迟


def get_magic_effect_fps_scale(特效):
    txz = 1
    if 特效 == "唧唧歪歪":
        txz = 1.15
    elif 特效 == "横扫千军" or 特效 == "浪涌":
        txz = 1.05
    elif 特效 == "反震" or 特效 == "防御":
        txz = 1.6
    elif 特效 == "捕捉开始"or 特效 == "暴击":
        txz = 1.55
    elif 特效 == "龙卷雨击1" or 特效 == "地裂火":
        txz = 1.15
    elif 特效 == "龙卷雨击2":
        txz = 1.5
    elif 特效 == "龙卷雨击3":
        txz = 1.0
    elif 特效 == "龙卷雨击4":
        txz = 1.15
    elif 特效 == "龙吟":
        txz = 1.45
    elif 特效 == "龙腾":
        txz = 1.75
    elif 特效 == "泰山压顶":
        txz = 1.0
    elif 特效 == "连环击":
        txz = 2.4
    elif 特效 == "天雷斩":
        txz = 1.6
    elif 特效 == "地狱烈火":
        txz = 1.6
    elif 特效 == "水漫金山" or 特效 == "鹰击" or 特效 == "上古灵符":
        txz = 1.48
    elif 特效 == "五雷轰顶":
        txz = 1
    elif 特效 == "天罗地网":
        txz = 0.85
    elif 特效 == "狮搏":
        txz = 1.4
    elif 特效 == "被击中"or 特效 == "飞砂走石" or 特效 == "二龙戏珠":
        txz = 1.28
    elif 特效 == "月光":
        txz = 1.3
    elif 特效 == "翻江搅海":
        txz = 3
    elif 特效 == "尘土刃":
        txz = 1.5
    elif 特效 == "泰山压顶1":
        txz = 1.0
    elif 特效 == "泰山压顶2":
        txz = 1.0
    elif 特效 == "泰山压顶3":
        txz = 1.0
    elif 特效 == "归元咒" or 特效 == "乾天罡气" or 特效 == "巨岩破" or 特效 == "推拿" or 特效 == "活血" or 特效 == "推气过宫":
        txz = 0.95
    elif 特效 == "惊心一剑" or 特效 == "牛刀小试" or 特效 == "力劈华山":
        txz = 1.05
    else:
        txz = 1.15
    return txz


def get_magic_attack_frame(name):
    """
    法术攻击帧默认为倒数第二帧, 如果多帧且间隔较长, 则有抖动效果(MagicEffect类中处理)
    若默认[-2, 0]或者间隔较短, 则说明法术效果是一次性击中, 没有抖动, 但是击退效果会有fade_in(BatterUnit类中实现)
    :param name: 法术名称
    :return:
    """
    攻击帧 = [-2]
    慢放 = True
    if name == '龙腾':
        攻击帧 = [-34, -6]
    elif name == '烈火':
        攻击帧 = [-12, -2]
    if 攻击帧[-1] - 攻击帧[0] > 2:
        慢放 = False
    return 攻击帧, 慢放


def get_buff_effect_position(name):
    front = True   # False在人物下层, True在人物上层
    on_top = False  # 是否在人物头顶
    py = (0, 0)  # 偏移量
    if name == "红灯" or name == "蓝灯" or name == "炼气化神":
        py = (0, 0)
        on_top = True
    elif name == "镇妖" or name == "失忆符" or name == "催眠符" or name == "落魄符" or name == "追魂符" or name == "炎护" or name == "含情脉脉" or name == "离魂符"  or name == "失心符" or name == "失魂符" or name == "碎甲符" or name == "一笑倾城" or name == "象形" or name == "似玉生香" or name == "乘风破浪" or name == "一苇渡江" or name == "逆鳞" or name == "夺魄令" or name == "百万神兵" or name == "护法紫丝":
        front = False
    elif name == "红袖添香":
        py = (10, 0)
    elif name == "天罗地网" or name == "乾坤玄火塔" or name == "苍白纸人" or name == "干将莫邪" or name == "莲步轻舞" or name == "如花解语":
        py = (1, 3)
        front = False
    elif name == "定身符":
        py = (5, 2)
        front = False
    elif name == "变身":
        py = (2, -31)
    elif name == "紧箍咒":
        py = (2, 0)
        on_top = True
    elif name == "普渡众生" or name == "生命之泉":
        py = (2, 0)
        on_top = True
    elif name == "血雨":
        py = (0, 0)
        on_top = True
    elif name == "鹰击" or name == "横扫千军" or name == "后发制人" or name == "破釜沉舟":
        front = False
    elif name == "凋零之歌":
        front = False
    return front, on_top, py
