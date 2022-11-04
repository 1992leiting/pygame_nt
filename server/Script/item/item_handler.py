from Script.common import constants as GL
from Script.common.common import *


def send_all_items(pid):
    sk = GL.SOCKETS[pid]
    send_data = [S_发送所有物品信息, {'数据': GL.ITEMS[pid]}]
    send(sk, send_data)
