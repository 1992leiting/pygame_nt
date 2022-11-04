from Script.common.constants import *


def start_tcp_server():
    """
    开启TCP服务器, 每个连接以线程方式运行
    :return:
    """
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, name='server', daemon=True).start()


ip, port = '0.0.0.0', 9093
server = socketserver.ThreadingTCPServer((ip, port), TCPHandler)
start_tcp_server()
# for npc in GL.NPCS:
#     print(npc, npc.name, npc.map_id, npc.mx, npc.my, npc.npc_type)

while True:
    cmd = input('服务端启动...\n>>>')
    if cmd.strip() == 'quit!':
        server.shutdown()
        server.server_close()
        break
