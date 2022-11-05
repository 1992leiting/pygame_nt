from Common.constants import *
import socketserver
import threading
# from Network.tcp_handler import TCPHandler
from Login.login import process_login
from multiprocessing import Process, Pipe


def start_tcp_server():
    """
    开启TCP服务器, 每个连接以线程方式运行
    :return:
    """
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, name='server', daemon=True).start()


if __name__ == '__main__':
    ip, port = '0.0.0.0', 9093
    # server = socketserver.ThreadingTCPServer((ip, port), TCPHandler)
    # start_tcp_server()

    conn_login, conn = Pipe()
    p_login = Process(target=process_login, args=(conn,))
    p_login.start()

    print('服务端启动...')
    while True:
        cmd = input('\n>>>')
        if cmd.strip() == 'quit!':
            server.shutdown()
            server.server_close()
            break
        elif 'login:' in cmd.strip():
            print('send to login:', cmd.strip('login:'))
            conn_login.send(cmd.strip('login:'))
