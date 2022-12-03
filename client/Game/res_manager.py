import os

from Common.constants import *
from io import BytesIO
import numpy as np
import copy
import time
import pygame
from PIL import Image
from threading import Thread

hash_list = {}
rsp_cache = {}  # key: wdf+hash


class Rs:
    def __init__(self):
        self.kx = 0
        self.ky = 0
        self.width = 0
        self.height = 0
        self.dir_cnt = 0
        self.palette16_data = []  # 565调色板原始数据, 256*2字节
        self.palette16 = []  # 565调色板, 256个RGB
        self.palette32 = []  # 888调色板, 256个RGBA
        self.frames = {}  # 帧队列,最多8个方向,内容为pygame.image

    def get_palette(self):
        # 565
        if self.palette16_data:
            for _byte in self.palette16_data:
                self.palette16.append(rgb565(int.from_bytes(_byte, 'little')))
        # 888
        self.palette32 = palette16_to_palette32(self.palette16)


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


class Wpal:
    """
    染色配置文件
    """
    def __init__(self):
        self.head = b'wpal'  # 文件头
        self.seg_num = 0  # 分段数量
        self.seg_index = []  # 每个分段对应的调色板位置
        self.seg_data = []  #

    def print(self):
        print('----------')
        print('head', self.head)
        print('seg num:', self.seg_num)
        # print(self.seg_data)
        for m in range(self.seg_num):
            for n in range(len(self.seg_data[m])):
                print(self.seg_data[m][n][0], self.seg_data[m][n][1], self.seg_data[m][n][2])
            print(' ')


def rgb565(color):
    r = (color >> 11) & 0x1F
    g = (color >> 5) & 0x3F
    b = color & 0x1F
    pixel = {'R': r, 'G': g, 'B': b}
    return pixel


def palette16_to_palette32(pal16: list):
    """
    565调色板信息转888调色板信息
    pal16: 256个RGB
    """
    pal32 = []
    for color in pal16:
        r, g, b = color['R'], color['G'], color['B']

        pixel = {'R': 0, 'G': 0, 'B': 0, 'Alpha': 0}
        pixel['R'] = (r << 3) | (r >> 2)
        pixel['G'] = (g << 2) | (g >> 4)
        pixel['B'] = (b << 3) | (b >> 2)
        pixel['Alpha'] = 255
        pal32.append(pixel)

    return pal32


def read_wpal(file_path):
    with open(file_path, 'rb') as f:
        pal = Wpal()
        head = f.read(4)
        if not head == pal.head:
            print('非法wpal文件:', file_path)
            return None
        pal.seg_num = int.from_bytes(f.read(4), byteorder='little')
        # 跳过
        for _ in range(1 + pal.seg_num):
            idx = read_int(f, 4)
            pal.seg_index.append(idx)
        for i in range(pal.seg_num):
            pal.seg_data.append([])
            solution_num = int.from_bytes(f.read(4), byteorder='little')
            # print('sol num:', solution_num)
            for j in range(solution_num):
                pal.seg_data[i].append([])
                c11 = int.from_bytes(f.read(4), byteorder='little')
                c12 = int.from_bytes(f.read(4), byteorder='little')
                c13 = int.from_bytes(f.read(4), byteorder='little')
                pal.seg_data[i][j].append([c11, c12, c13])
                # print(c11, c12, c13)
                c21 = int.from_bytes(f.read(4), byteorder='little')
                c22 = int.from_bytes(f.read(4), byteorder='little')
                c23 = int.from_bytes(f.read(4), byteorder='little')
                pal.seg_data[i][j].append([c21, c22, c23])
                # print(c21, c22, c23)
                c31 = int.from_bytes(f.read(4), byteorder='little')
                c32 = int.from_bytes(f.read(4), byteorder='little')
                c33 = int.from_bytes(f.read(4), byteorder='little')
                pal.seg_data[i][j].append([c31, c32, c33])
                # print(c31, c32, c33)
    return pal


def palette_modulate(ori_pal16: list, wpal_file, segment, solution):
    """
    进行调色板调色
    ori_pal16: 资源文件的原始调色板, 256个RGB
    wpal_file: wpal文件路径
    segment: 部位
    solution: 染色方案

    return: 调色之后的新调色板
    """
    pal = read_wpal(wpal_file)
    new_palette = copy.deepcopy(ori_pal16)
    C11, C12, C13 = pal.seg_data[segment][solution][0]
    C21, C22, C23 = pal.seg_data[segment][solution][1]
    C31, C32, C33 = pal.seg_data[segment][solution][2]

    for i in range(pal.seg_index[segment], pal.seg_index[segment + 1]):
        R = ori_pal16[i]['R']
        G = ori_pal16[i]['G']
        B = ori_pal16[i]['B']

        R2 = (R * C11 + G * C12 + B * C13) // 256
        G2 = (R * C21 + G * C22 + B * C23) // 256
        B2 = (R * C31 + G * C32 + B * C33) // 256

        R2 = min(R2, 31)
        G2 = min(G2, 63)
        B2 = min(B2, 31)

        new_palette[i]['R'] = R2
        new_palette[i]['G'] = G2
        new_palette[i]['B'] = B2

    return new_palette, (pal.seg_index[segment], pal.seg_index[segment + 1])


def modulate_img_by_palette(img, ori_pal32: list, new_pal32: list):
    """
    pygame image染色
    """
    # ---暴力循环法1---
    # w, h = img.get_size()
    # pix_array = {}
    # for x in range(w):
    #     for y in range(h):
    #         img_pix = img.get_at((x, y))
    #         if img_pix != (0, 0, 0, 0):
    #             pix_array[(x, y)] = (img_pix[0], img_pix[1], img_pix[2])  # TODO:这一步很慢
    # for pos, pix in pix_array.items():
    #     for index in range(256):
    #         ori_pal32_pix = ori_pal32[index]
    #         if ori_pal32_pix != new_pal32[index]:
    #             ori_pal32_color = (ori_pal32_pix['R'], ori_pal32_pix['G'], ori_pal32_pix['B'])
    #             if pix == ori_pal32_color:
    #                 r = new_pal32[index]['R']
    #                 g = new_pal32[index]['G']
    #                 b = new_pal32[index]['B']
    #                 img.set_at(pos, (r, g, b, 255))

    # ---暴力循环法2---
    # w, h = img.get_size()
    # for x in range(w):
    #     for y in range(h):
    #         img_pix = img.get_at((x, y))
    #         if img_pix != (0, 0, 0, 0):
    #             for index in range(256):
    #                 r, g, b, a = ori_pal32[index]['R'], ori_pal32[index]['G'], ori_pal32[index]['B'], 255
    #                 if img_pix == (r, g, b, a):
    #                     rr, gg, bb, aa = new_pal32[index]['R'], new_pal32[index]['G'], new_pal32[index]['B'], 255
    #                     img.set_at((x, y), (rr, gg, bb, 255))
    #                     break

    # ---pixelarray替换法---
    new_img = img.copy()
    pa = pygame.PixelArray(new_img)
    for index in range(256):
        ori_color = ori_pal32[index]['R'], ori_pal32[index]['G'], ori_pal32[index]['B'], 255
        new_color = new_pal32[index]['R'], new_pal32[index]['G'], new_pal32[index]['B'], 255
        if ori_color != new_color:
            pa.replace(ori_color, new_color)
    pa.close()
    return new_img

    # ---PIL-numpy法---
    # img_bytes = img.get_buffer().raw
    # # pil_img = Image.frombytes('RGBA', (w, h), img_bytes)
    # # pil_img.show()
    # # data = np.array(pil_img)
    # data = np.frombuffer(img_bytes, np.int8).copy()
    # data = data.reshape((w, h, 4))
    # for index in range(256):
    #     ori_pal32_pix = ori_pal32[index]
    #     data[(data == (0, 0, 0, 0)).all(axis=-1)] = (255, 255, 255, 255)
    # img = Image.fromarray(data, 'RGBA')
    # img_data = img.tobytes()
    # img = pygame.image.frombuffer(img_data, (w, h), 'RGBA')
    # # img.show()


def modulate_animation_by_palette(ani, wpal_file, ori_pal16, recipe):
    """
    Animation类染色, 完成后设置标志位
    """
    t = time.time()
    ori_pal32 = palette16_to_palette32(ori_pal16)
    new_pal16, _ = palette_modulate(ori_pal16, wpal_file, 0, recipe[0])
    new_pal16, _ = palette_modulate(new_pal16, wpal_file, 1, recipe[0])
    new_pal16, _ = palette_modulate(new_pal16, wpal_file, 2, recipe[0])
    new_pal32 = palette16_to_palette32(new_pal16)
    for j in range(len(ani.frames)):
        ani.frames[j] = modulate_img_by_palette(ani.frames[j], ori_pal32, new_pal32)
    ani.is_modulated = True
    dt = time.time() - t
    # print('animation染色时间:{}ms'.format(int(dt*1000)))


def bytes_to_image(bytes_data):
    """
    将资源文件中的bytes数据转换为pygame.image
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
    ani8d.clear_children()
    res = read_rsp(rsp_file, hash_id)
    for i in range(res.dir_cnt):
        frames = res.frames[i]
        ani = Animation()
        ani.frames = []
        ani.kx, ani.ky = res.kx, res.ky
        ani.width, ani.height = res.width, res.height
        for img in frames:
            ani.frames.append(img)
        ani8d.add_child(str(i), ani)
    ani8d.palette16 = res.palette16
    ani8d.palette32 = res.palette32
    ani8d.width, ani8d.height = res.width, res.height


def fill_image_rect(img, rsp_file, hash_id):
    res = read_rsp(rsp_file, hash_id)
    img.image = res.frames[0][0]
    img.raw_image = img.image.copy()
    img.kx, img.ky = res.kx, res.ky
    # 没有指定宽高则取素材宽高, 否则进行裁切
    crop = False
    if img.width == 0:
        img.width = res.width
        w = 0
    else:
        crop = True
        w = img.width
    if img.height == 0:
        img.height = res.height
        h = 0
    else:
        crop = True
        h = img.height
    if crop:
        img.auto_sizing(w, h)
    return img


def fill_magic_effect(eff, name):
    from Database.effect_res import get_effect
    _hash, _rsp = get_effect(name)
    fill_animation8d(eff, _rsp, int(_hash))


def read_int(f, length, bo='little'):
    bts = f.read(length)
    if bo == 'little':
        return int.from_bytes(bts, byteorder='little')
    else:
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
        if hash_id.isdigit():
            hash_id = int(hash_id)
        else:
            hash_id = hash_id.replace('0X', '0x')
            if '0x' not in hash_id:
                hash_id = '0x' + hash_id
            hash_id = int(hash_id, 16)
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

            for _ in range(256):
                res.palette16_data.append(rspf.read(2))  # 565调色板原始数据, 256*2字节
            res.get_palette()
            for dir_num in range(res.dir_cnt):
                res.frames[dir_num] = []
                fr_cnt = read_int(rspf, 2)
                for j in range(fr_cnt):
                    fr_size = read_int(rspf, 4)
                    fr_data = rspf.read(fr_size)
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
        mapx.width = read_int(mapf, 2, 'big')
        mapx.height = read_int(mapf, 2, 'big')
        jpg_data_len = read_int(mapf, 4, 'big')
        jpg_data = mapf.read(jpg_data_len)
        mapx.jpg = bytes_to_image(jpg_data)

        mapx.navi_width = read_int(mapf, 2, 'big')
        mapx.navi_height = read_int(mapf, 2, 'big')
        navi_array = []
        for i in range(mapx.navi_width):
            row = []
            for j in range(mapx.navi_height):
                num = read_int(mapf, 1, 'big')
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

        mapx.mask_cnt = read_int(mapf, 2, 'big')
        for i in range(mapx.mask_cnt):
            # print(i)
            mask = MapMask()
            mask.id = read_int(mapf, 2, 'big')
            mask.x = read_int(mapf, 2, 'big')
            mask.y = read_int(mapf, 2, 'big')
            mask.width = read_int(mapf, 2, 'big')
            mask.height = read_int(mapf, 2, 'big')
            mask_data_len = read_int(mapf, 4, 'big')
            mask_data = mapf.read(mask_data_len)
            mask.img = bytes_to_image(mask_data)
            mapx.masks.append(mask)
    print('read mapx:', str(map_id), ' ', time.time() - t, 's')
    return mapx


get_hash_list()
