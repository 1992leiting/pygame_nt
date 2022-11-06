from Common import constants as GL
from Common.common import *
import socket
import json


def send_sys_error(sk: socket.socket, text, tp='错误'):
    send_data = [S_系统错误, {'类型': tp, '内容': text}]
    send(sk, send_data)


def create_account(acc_name):
    pass
