class GatewaySocket:
    def __init__(self):
        self.cur_socket = None


gateway_socket = GatewaySocket()
REDIS_AUTO_SAVE_INTERVAL = 60
GATEWAY_SERVER = ('127.0.0.1', 9093)
GAME_SERVER_REGISTER_CMD = 'game-server-U84JFNF9845N329FJRM44IF84H'  # 每次game server进程向gateway注册时的cmd
DATA_PATH = 'data/'
ACCOUNT_SUMMARY_PATH = DATA_PATH + 'account_summary.json'
