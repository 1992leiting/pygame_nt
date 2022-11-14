from Common.constants import *
from io import BytesIO
import numpy as np
import time
import pygame
from PIL import Image

hash_list = {}
rsp_cache = {}  # key: wdf+hash


class Rs:
    def __init__(self):
        self.kx = 0
        self.ky = 0
        self.width = 0
        self.height = 0
        self.dir_cnt = 0
        self.frames = {}  # 帧队列,最多8个方向,内容为pygame.image


class Mask:
    def __init__(self):
        self.id = 0
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.img = None  # pygame.image


class Mapx:
    def __init__(self):
        self.map_id = 0
        self.width = 0
        self.height = 0
        self.jpg = None  # pygame.image

        self.navi_width = 0
        self.navi_height = 0
        self.navi = None

        self.mask_cnt = 0
        self.masks = []  # 所有的遮罩, 类型为MapMask


def bytes_to_image(bytes_data):
    """
    将资源文件中的bytes数据转换为pygame.image
    :param bytes_data:
    :return:
    """
    data = BytesIO()
    data.write(bytes_data)
    data.seek(0)
    img = pygame.image.load(data).convert_alpha()
    return img


def fill_res(node, rsp_file, hash_id):
    from Node.button import Button
    from Node.image_rect import ImageRect
    from Node.progressbar import ProgressBar
    from Node.animation import Animation8D
    from Node.emoji import Emoji
    if type(node) == Button:
        fill_button(node, rsp_file, hash_id)
    elif type(node) == Animation8D:
        fill_animation8d(node, rsp_file, hash_id)
    elif type(node) == ImageRect or type(node) == ProgressBar:
        fill_image_rect(node, rsp_file, hash_id)
    elif type(node) == Emoji:
        fill_emoji(node, rsp_file, hash_id)
    else:
        print('Fill unknown res: ', str(type(node)))


def fill_emoji(emoji, rsp_file, hash_id):
    res = read_rsp(rsp_file, hash_id)
    frames = res.frames[0]  # 只使用第一个方向的帧
    emoji.width, emoji.height = res.width, res.height
    emoji.kx, emoji.ky = res.kx, res.ky
    for img in frames:
        emoji.frames.append(img)
    emoji.frame_num = len(frames)
    emoji.cur_frame = frames[0]


def fill_button(btn, rsp_file, hash_id):
    res = read_rsp(rsp_file, hash_id)
    frames = res.frames[0]  # 只使用第一个方向的帧
    btn.img_normal = frames[0]
    btn.img_hover = frames[0]
    btn.img_pressed = frames[0]
    btn.img_disable = frames[0]
    if len(frames) >= 2:
        btn.img_pressed = frames[1]
    else:
        btn.is_single_frame = True
    if len(frames) >= 3:
        btn.img_hover = frames[2]
    if len(frames) >= 4:
        btn.img_disable = frames[3]
    btn.width, btn.height = res.width, res.height
    btn.kx, btn.ky = res.kx, res.ky


def fill_animation8d(ani8d, rsp_file, hash_id):
    from Node.animation import Animation
    res = read_rsp(rsp_file, hash_id)
    for i in range(res.dir_cnt):
        frames = res.frames[i]
        ani = Animation()
        ani.kx, ani.ky = res.kx, res.ky
        ani.width, ani.height = res.width, res.height
        for img in frames:
            ani.frames.append(img)
        ani.frame_num = len(ani.frames)
        ani8d.add_child(str(i), ani)
        if i == 0:
            ani8d.cur_animation = ani8d.child(str(i))
    ani8d.width, ani8d.height = res.width, res.height


def fill_image_rect(img, rsp_file, hash_id):
    res = read_rsp(rsp_file, hash_id)
    img.image = res.frames[0][0]
    img.kx, img.ky = res.kx, res.ky
    img.width, img.height = res.width, res.height


def fill_magic_effect(eff, name):
    from Database.effect_res import get_effect
    _hash, _rsp = get_effect(name)
    fill_animation8d(eff, _rsp, int(_hash))


def read_int(f, length):
    bts = f.read(length)
    return int.from_bytes(bts, byteorder='big')


def get_hash_list():
    for file in os.listdir(rsp_dir):
        if file.endswith('.rsp'):
            hash_list[file] = {}
            file_path = rsp_dir + file
            with open(file_path, 'rb') as rspf:
                pck_flag = read_int(rspf, 2)
                file_cnt = read_int(rspf, 2)

                for i in range(file_cnt):
                    rs_hash = read_int(rspf, 8)
                    rs_offset = read_int(rspf, 4)
                    hash_list[file][rs_hash] = rs_offset
            print('初始化资源文件:', file)


def read_rsp(rsp_file, hash_id):
    import time
    t = time.time()
    res = Rs()
    # 判断文件和hash是否存在
    if rsp_file not in hash_list:
        print('资源文件不存在: ', rsp_file)
        return res
    if type(hash_id) == str:
        hash_id = hash_id.replace('0X', '0x')
        if '0x' not in hash_id:
            hash_id = '0x' + hash_id
        hash_id = hex(hash_id)
    hash_id = int(hash_id)
    if hash_id not in hash_list[rsp_file]:
        print('hash不存在: ', rsp_file, hash_id)
        return read_rsp('wzife.rsp', 0x20F3E242)  # 问号
    # 检查资源池是否已经缓存
    key = str(rsp_file + str(hash_id))
    if key in rsp_cache:
        return rsp_cache[key]['res']
    else:
        file_path = rsp_dir + rsp_file
        with open(file_path, 'rb') as rspf:
            rspf.seek(hash_list[rsp_file][hash_id])
            res.kx = read_int(rspf, 2)
            if res.kx > 1000:
                res.kx = -65536 + res.kx
            res.ky = read_int(rspf, 2)
            if res.ky > 1000:
                res.ky = -65536 + res.ky
            res.width = read_int(rspf, 2)
            res.height = read_int(rspf, 2)
            res.dir_cnt = read_int(rspf, 2)
            for dir_num in range(res.dir_cnt):
                res.frames[dir_num] = []
                fr_cnt = read_int(rspf, 2)
                for j in range(fr_cnt):
                    fr_size = read_int(rspf, 4)
                    fr_data = rspf.read(fr_size)
                    # TODO: 测试转换RGB
                    # with open('tmp.png', 'wb') as f:
                    #     f.write(fr_data)
                    # pil_image = Image.open('tmp.png')
                    # r, g, b, a = pil_image.split()
                    # pil_image = Image.merge('RGBA', (r, g, r, a))
                    # pil_image.save('tmp.png')
                    # with open('tmp.png', 'rb') as f:
                    #     fr_data = f.read()

                    img = bytes_to_image(fr_data)
                    res.frames[dir_num].append(img)
        rsp_cache[key] = {'time': time.time(), 'res': res}
    return res


def read_mapx(map_id):
    print('read map:', map_id)
    import time
    from Node.map_mask import MapMask
    t = time.time()
    mapx = Mapx()
    mapx.map_id = map_id
    file_path = map_dir + str(map_id) + '.mapx'
    with open(file_path, 'rb') as mapf:
        map_flag = mapf.read(4)
        mapx.width = read_int(mapf, 2)
        mapx.height = read_int(mapf, 2)
        jpg_data_len = read_int(mapf, 4)
        jpg_data = mapf.read(jpg_data_len)
        mapx.jpg = bytes_to_image(jpg_data)

        mapx.navi_width = read_int(mapf, 2)
        mapx.navi_height = read_int(mapf, 2)
        navi_array = []
        for i in range(mapx.navi_width):
            row = []
            for j in range(mapx.navi_height):
                num = read_int(mapf, 1)
                if num == 0:
                    num = 9999
                else:
                    num = 1
                row.append(num)
            navi_array.append(row)
        mapx.navi = np.array(navi_array).T.astype(np.float32)

        # 存excel
        # df = pd.DataFrame(mapx.navi)
        # df.to_excel('navi.xlsx', index=None)

        mapx.mask_cnt = read_int(mapf, 2)
        for i in range(mapx.mask_cnt):
            # print(i)
            mask = MapMask()
            mask.id = read_int(mapf, 2)
            mask.x = read_int(mapf, 2)
            mask.y = read_int(mapf, 2)
            mask.width = read_int(mapf, 2)
            mask.height = read_int(mapf, 2)
            mask_data_len = read_int(mapf, 4)
            mask_data = mapf.read(mask_data_len)
            mask.img = bytes_to_image(mask_data)
            mapx.masks.append(mask)
    print('read mapx:', str(map_id), ' ', time.time() - t, 's')
    return mapx


get_hash_list()
