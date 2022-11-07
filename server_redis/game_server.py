from common.server_process import game_server_client
from common.common import *
from common.constants import *


def start_game_server():
    game_server_client.connect()
    game_server_client.start()

    send(game_server_client.socket, GAME_SERVER_REGISTER_CMD, {})


start_game_server()
