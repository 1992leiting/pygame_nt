import random
from common.socket_id import *
from common.common import *
from common.constants import *
from common.server_process import server


def get_npc_in_scene(pid, map_id=0):
    if not map_id:
        map_id = rget(pid, CHAR, '地图')
    npcs = []

    # 脚本方式
    # for npc in NPCS:
    #     if npc.map_id == map_id:
    #         npc_data = {
    #             'npc_id': npc.npc_id,
    #             '名称': npc.name,
    #             '称谓': npc.title,
    #             '模型': npc.model,
    #             'mx': npc.mx,
    #             'my': npc.my,
    #             '方向': npc.direction,
    #             '地图': npc.map_id,
    #             'NPC类型': npc.npc_id
    #         }

    # csv方式
    i = 0
    for npc in NPCS.values():
        if int(npc['地图']) == map_id:
            i += 1
            npc_data = {
                'id': i,
                '名称': npc['名称'],
                '称谓': npc['称谓'],
                '模型': npc['模型'],
                'mx': npc['x'],
                'my': npc['y'],
                '方向': npc['方向'],
                '地图': npc['地图'],
                'NPC类型': npc['类型']
            }
            npcs.append(npc_data)
    return npcs


def player_enter_scene(pid, map_id):
    if not map_id:
        map_id = rget(pid, CHAR, '地图')
    # 发送所有npc
    # for npc_data in get_npc_in_scene(pid, map_id):
    #     send2pid(pid, S_NPC数据, npc_data)
    # 取其他玩家数据
    for _pid in get_players_in_scene(pid, map_id):
        player_data = rget(_pid, CHAR)
        send2pid(pid, S_玩家数据, player_data)
    # 通知其他玩家
    my_data = rget(pid, CHAR)
    for _pid in get_players_in_scene(pid, map_id):
        send2pid(_pid, S_玩家数据, my_data)


def player_leave_scene(pid, map_id):
    pass


def player_set_path_request(pid, path: list):
    """
    玩家有移动路径时, 判断是否能移动
    :param pid:
    :param path:
    :return:
    """
    print('player set path:', pid, path)
    # TODO
    send2pid(pid, S_发送路径, dict(路径=path))
    # 如果移动(path非空), 则广播给同场景玩家
    if path:
        for _pid in get_players_in_scene(pid, None):
            send2pid(_pid, S_玩家寻路, dict(玩家=pid, 路径=path))


def player_speak(pid, ch, text):
    map_id = rget(pid, CHAR, '地图')
    if ch == '当前':
        print('发言给:', get_players_in_scene(pid, map_id, True))
        for _pid in get_players_in_scene(pid, map_id, True):
            send2pid(_pid, S_频道发言, dict(频道=ch, 内容=text, 名称=rget(pid, CHAR, '名称')))
            send2pid(_pid, S_角色发言显示, dict(player=pid, 内容=text))


def scene_transfer(pid, map_id, x, y):
    send_data = dict(map_id=map_id, x=x, y=y)
    send2pid(pid, S_地图传送, send_data)
