from Common.constants import *
import socketserver
import threading
from Network.tcp_handler import TCPHandler
from Login.login import ProcessLogin
from Game.game import ProcessGame
from Map.map import ProcessMap
from Chat.chat import ProcessChat
from Battle.battle import ProcessBattle
from multiprocessing import Lock
from Common.common import *


def start_tcp_server():
    """
    开启TCP服务器, 每个连接以线程方式运行
    :return:
    """
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, name='GATEWAY', daemon=True).start()


if __name__ == '__main__':
    ip, port = '0.0.0.0', 9093
    server = socketserver.ThreadingTCPServer((ip, port), TCPHandler)
    start_tcp_server()

    # p_lock = Lock()
    #
    # p_login = ProcessLogin(p_lock)
    # p_login.start()
    # p_game = ProcessGame(p_lock)
    # p_game.start()
    # p_map = ProcessMap(p_lock)
    # p_map.start()
    # p_chat = ProcessChat(p_lock)
    # p_chat.start()
    # p_battle = ProcessBattle(p_lock)
    # p_battle.start()
