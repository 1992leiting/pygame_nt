import socketserver
import threading
import orjson
from common.common import send
from common.constants import *
from common.socket_id import *
from common.constants import gateway_socket
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
        self.redis_server = None  # redis监控进程,独立运行,自动保存redis数据
        self.redis_conn = None  # 每个进程各自的redis连接
        self.gateway = None  # 网关进程


server = Server()


class RedisClient:
    def __init__(self):
        self.conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)



