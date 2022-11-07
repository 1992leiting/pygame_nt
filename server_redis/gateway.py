from common.server_process import GatewayServer, redis_client
from common.common import *
from common.constants import *
import threading
import socketserver
import os


def start_tcp_server():
    """
    开启TCP服务器, 每个连接以线程方式运行
    :return:
    """
    gateway_server.daemon_threads = True
    threading.Thread(target=gateway_server.serve_forever, name='GATEWAY', daemon=True).start()


if __name__ == '__main__':
    # 启动网关tcp服务
    gateway_server = socketserver.ThreadingTCPServer(GATEWAY_SERVER, GatewayServer)  # 网关进程
    start_tcp_server()
    sprint('网关启动成功')

    # 连接redis并清除数据
    redis_client.conn.flushall()

    sprint('启动子进程...')
    # os.system('start python')
    os.system('start python redis_server.py')
    os.system('start python game_server.py')
    os.system('start python game_server.py')
    os.system('start python game_server.py')

    while True:
        try:
            cmd = input('')
        except:
            break
