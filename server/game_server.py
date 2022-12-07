from common.common import *
from common.constants import *
import threading
import socket
from uuid import uuid4
from common.socket_id import *
import sys
import logging
import traceback
from scene.scene_handler import *
from scene.dialog_handler import *
from player.player_handler import *


def player_cmd_handler(msg):
    pid = msg['pid']  # 玩家id
    cmd = msg['cmd']
    # print('game server recv:', msg)

    if cmd == C_更新坐标:
        x, y, map_id = msg['x'], msg['y'], msg['mapid']
        pdata = server.players[pid]
        pdata['mx'], pdata['my'], pdata['地图'] = x, y, map_id
    elif cmd == C_进入场景:
        map_id = msg['map_id']
        player_enter_scene(pid, map_id)
    elif cmd == C_发送路径:
        path = msg['路径']
        # print('发送路径,', pid, path)
        player_set_path_request(pid, path)
    elif cmd == C_角色发言:
        ch = msg['频道']
        text = msg['内容']
        player_speak(pid, ch, text)
    elif cmd == C_点击NPC:
        npc_id = msg['id']
        trigger_npc_dialog(pid, npc_id)
    elif cmd == C_传送点传送:
        portal_id = msg['portal_id']
        if str(portal_id) in PORTALS:
            target_map = int(PORTALS[str(portal_id)]['目的地'])
            target_x = int(PORTALS[str(portal_id)]['目的地x'])
            target_y = int(PORTALS[str(portal_id)]['目的地y'])
            scene_transfer(pid, target_map, target_x, target_y)
    elif cmd == C_对话选项:
        print('对话选项:', msg)
        map_id = msg['map_id']  # 对话发生时的地图id
        name = msg['name']  # 对话对象的名称
        option = msg['option']
        id = msg['id']
        dialog_type = msg['type']
        if dialog_type == 'npc':
            trigger_npc_response(pid, id, option)
    elif cmd == C_角色升级:
        player_level_up(pid)
    elif cmd == C_攻击玩家:
        pass

