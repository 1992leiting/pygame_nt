import os
from Script.common.common import *
import pandas as pd

# 数据库
PORTALS = pd.read_csv('Script/database/scene_portal.csv')
DESTINATIONS = pd.read_csv('Script/database/portal_destination.csv', index_col='名称')
XA_PORTALS = pd.read_csv('Script/database/XA_portals.csv')

# 所有玩家数据,索引均为玩家id
PLAYERS = {}        # 所有玩家数据
ITEMS = {}          # 所有玩家物品数据
SOCKETS = {}        # 所有玩家的网络socket
TEAMS = {}          # 所有队伍信息

# 对话数据
DIALOGUE_HISTORY = {}

# 玩家数据的内存空间大小
GLOBAL_MEM_SIZE = 1 * 1024 * 1024  # 1MB

# 所有NPC, {地图:[npc]}
NPCS = []
