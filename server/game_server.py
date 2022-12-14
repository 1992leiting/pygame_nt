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
        server.players[pid][CHAR]['mx'], server.players[pid][CHAR]['my'], server.players[pid][CHAR]['地图'] = x, y, map_id
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
        name = msg['name']
        dialog_type = msg['type']
        if dialog_type == 'npc':
            trigger_npc_response(pid, id, name, option)
    elif cmd == C_角色升级:
        player_level_up(pid)
    elif cmd == C_攻击玩家:
        from battle.battle_start import start_pvp
        target = msg['target_pid']
        map_id = msg['map_id']
        x, y = msg['x'], msg['y']
        # player_start_pvp_request(pid, target)
        start_pvp(B_玩家切磋, pid, target)
    elif cmd == C_战斗命令:
        print('战斗命令', msg)
        battle = get_pid_battle(pid)
        if battle:
            battle.set_unit_cmd_by_pid(pid, msg)
    elif cmd == C_战斗回合执行完成:
        print('战斗执行完成:', pid)
        battle = get_pid_battle(pid)
        if battle:
            battle.set_unit_param_by_pid(pid, '战斗执行完成', True)
