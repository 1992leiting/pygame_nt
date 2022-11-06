from common.server_process import game_server_client


def start_game_server():
    game_server_client.connect()
    game_server_client.start()


start_game_server()
