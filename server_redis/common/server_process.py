import socketserver
import threading
from common.constants import *
from common.socket_id import *
import socket
import redis
import time
import os


class Server:
    """
    空类, 存放服务器的各种进程
    """
    def __init__(self):
        self.game_server = None  # game server进程
        self.redis_server = None  # redis监控线程,独立运行,自动保存redis数据
        self.redis_conn = None  # 每个进程各自的redis连接
        self.gateway = None  # 网关进程

        self.tmp_client_socket = {}  # 非服务器/非玩家的临时socket
        self.logged_socket = []  # 已经登陆的socket连接

        # self.npcs = []  # 所有的npc数据
        self.npc_objects = {}  # 所有的npc对象, key:npc_id, value:NPC类


server = Server()


class RedisClient:
    def __init__(self):
        self.conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)



