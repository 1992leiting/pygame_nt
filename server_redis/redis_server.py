from common.server_process import redis_server


if __name__ == '__main__':
    redis_server.setup()
    redis_server.start()
