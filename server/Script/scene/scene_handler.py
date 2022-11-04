from Script.common import constants as GL
from Script.common.common import *
import random


class NPC:
    def __init__(self) -> None:
        self.npc_id = 0
        self.name = 'NPC'
        self.title = None
        self.model = '男人_苦力'
        self.mx, self.my = 0, 0
        self.direction = 0  # 方向, 0 ↘, 1 ↓, 2 ↙, 3 →, 4 ←, 5 ↗, 6 ↑, 7 ↖
        self.map_id = 1001
        self.npc_type = '普通'  # 普通, 商业, 特殊, 传送, 任务
        self.dialogue = {'contents': ['你找我有事吗?'], 'options': []}

    def talk(self, id, option=None):
        cont = random.sample(self.dialogue['contents'], 1)
        op = self.dialogue['options']

        send_data = [S_发送NPC对话, {'模型': self.model, 'id': self.npc_id, '名称': self.name, '对话': cont, '选项': op}]
        sk = GL.SOCKETS[id]
        GL.DIALOGUE_HISTORY[id] = send_data
        send(sk, send_data)
        

def load_players_in_scene(pid):
    """
    以该id玩家为中心加载同场景玩家
    """
    sk = GL.SOCKETS[pid]
    player = GL.PLAYERS[pid]

    players = get_players_in_scene(pid)
    for p in players:
        # 玩家数据一个个发送
        send_data = [S_加载玩家, {'玩家': p}]
        send(sk, send_data)


def load_npcs_in_scene(pid):
    """
    加载改玩家所在场景的所有NPC
    """
    sk = GL.SOCKETS[pid]
    map_id = GL.PLAYERS[pid]['地图']
    for npc in GL.NPCS:
        if npc.map_id == map_id:
            npc_data = {
                'npc_id': npc.npc_id,
                '名称': npc.name,
                '称谓': npc.title,
                '模型': npc.model,
                'mx': npc.mx,
                'my': npc.my,
                '方向': npc.direction,
                '地图': npc.map_id,
                'NPC类型': npc.npc_id
            }
            send_data = [S_发送场景NPC, {'npc': npc_data}]
            # print('发送场景NPC:', npc.name)
            send(sk, send_data)


def add_player_in_scene(pid):
    """
    通知该场景的所有玩家此id进入场景
    """
    players = get_players_in_scene(pid)
    for p in players:
        sk = GL.SOCKETS[p['id']]
        send(sk, [S_进入场景, {'玩家': GL.PLAYERS[pid]}])
        # print('通知:', p['id'], pid, '进入场景')


def remove_player_from_scene(pid):
    """
    通知该场景的所有玩家此id离开场景
    """
    players = get_players_in_scene(pid)
    for p in players:
        sk = GL.SOCKETS[p['id']]
        send(sk, [S_离开场景, {'id': pid}])


def get_npc_talk(pid, data):
    # print('get npc talk:', pid, data)
    """
    获取NPC对话
    :param id: 人物id
    :param data: 数据, 包括npc_id, 选项等
    """
    npc_id = data['npc_id']
    name = data['名称']
    op = None
    if '选项' in data:
        op = data['选项']
    for npc in GL.NPCS:
        if npc.npc_id == npc_id and npc.name == name:
            # print(id, 'talk to:', npc.name)
            npc.talk(pid, op)


def send_dialogue_with_last(pid, data):
    """
    发送对话, 对象为上一次发送时的对象
    """
    pass


def clear_items_in_scene(pid):
    """
    清除该玩家所在场景的所有character, 包括NPC, 其他玩家, 传送点等
    """
    sk = GL.SOCKETS[pid]
    send(sk, [S_清除场景人物, {}])


def player_enter_scene(pid):
    """
    玩家进入场景的一系列操作
    """
    clear_items_in_scene(pid)        # 清除场景上的NPC和玩家
    add_player_in_scene(pid)        # 通知其他玩家自己进入场景
    load_players_in_scene(pid)      # 加载场景上其他玩家
    load_npcs_in_scene(pid)         # 加载场景上的NPC
    load_portals_in_scene(pid)      # 加载场景上的传送点


def scene_transfer(pid, map_id, x, y, tp=None):
    """
    场景传送
    :param id: 玩家id
    :param map_id: 目的地地图id
    :param x, y: 目的地坐标
    :param tp: 传送类型, npc传送, 道具传送, 被动传送(任务等触发自动传送)
    """
    remove_player_from_scene(pid)

    GL.PLAYERS[pid]['地图'] = map_id
    GL.PLAYERS[pid]['mx'], GL.PLAYERS[pid]['my'] = x, y
    sk = GL.SOCKETS[pid]
    send_data = [S_场景传送, {'地图': map_id, 'mx': x, 'my': y, '类型': tp}]
    send(sk, send_data)

    player_enter_scene(pid)


def load_portals_in_scene(pid):
    map_id = GL.PLAYERS[pid]['地图']
    sk = GL.SOCKETS[pid]

    # 飞蛾传送圈数据写法
    # portal_table = GL.PORTALS[GL.PORTALS['地图'] == map_id]  # 当前地图传送圈
    # for row in portal_table.iterrows():
    #     send_data = [S_发送传送点, {'x': row[1][2], 'y': row[1][3], '名称': row[1][4]}]
    #     send(sk, send_data)
    #     GL.PLAYERS[pid]['传送完成'] = True  # 避免重复发送

    # 笑傲传送圈数据写法
    portal_table = GL.XA_PORTALS[GL.XA_PORTALS['原地图'] == map_id]  # 当前地图传送圈
    # print('发送传送圈:', portal_table)
    for row in portal_table.iterrows():
        send_data = [S_发送传送点, {'x': row[1][2], 'y': row[1][3], 'id': row[1][0]}]
        send(sk, send_data)
        GL.PLAYERS[pid]['传送完成'] = True  # 避免重复发送


def portal_transfer(pid, portal_id):
    print('portal trans:', pid, portal_id)
    try:
        tmp = GL.XA_PORTALS.copy()
        tmp = tmp.set_index('id')
        des = tmp.loc[portal_id].to_list()
        map_id, x, y = int(des[3]), des[4], des[5]
        scene_transfer(pid, map_id, x, y)
    except BaseException as e:
        raise e
        GL.PLAYERS[pid]['传送完成'] = True
        print('portal err:', str(e))


def update_player_data_in_scene(pid, update_id, update_data):
    """
    向同场景玩家刷新某个玩家的数据
    pid: 中心玩家
    update_id: 要刷新的玩家id
    update_data: 要刷新的玩家数据
    """
    players = get_players_in_scene(pid, include_self=True)
    for p in players:
        sk = GL.SOCKETS[p['id']]
        send_data = [S_刷新玩家数据, {'id': update_id, '数据': update_data}]
        send(sk, send_data)
