from common.server_process import server
import threading
import os
from common.constants import *
import redis
import time


class RedisServer(threading.Thread):
    def __init__(self):
        super(RedisServer, self).__init__()
        self.conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
        self.timer = time.time() + REDIS_AUTO_SAVE_INTERVAL

    def setup(self):
        from common.common import dict2file, file2dict, redis_set_data
        # 没有account summary file则创建
        account_summary_file = os.path.join(DATA_PATH, 'account_summary.json')
        if not os.path.exists(account_summary_file):
            data = {}
            dict2file(data, account_summary_file)

    def run(self):
        from common.common import sprint
        sprint('redis watcher启动...')
        while True:
            if time.time() > self.timer:
                self.timer = time.time() + REDIS_AUTO_SAVE_INTERVAL
                self.save()

    def redis_save(self, key):
        from common.common import redis_get_data, dict2file, redis_get_hash_data
        if key == 'account_summary':
            data = redis_get_data(self.conn, key)
            dict2file(data, ACCOUNT_SUMMARY_PATH)
        else:  # 玩家数据数据
            pid = key
            # 角色数据
            data = redis_get_hash_data(self.conn, key, 'char')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'char.json')
            dict2file(data, file)
            # 物品数据
            data = redis_get_hash_data(self.conn, key, 'item')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'item.json')
            dict2file(data, file)
            # 物品仓库数据
            data = redis_get_hash_data(self.conn, key, 'item_warehouse')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'item_warehouse.json')
            dict2file(data, file)
            # 宠物数据
            data = redis_get_hash_data(self.conn, key, 'pet')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'pet.json')
            dict2file(data, file)
            # 宠物仓库数据
            data = redis_get_hash_data(self.conn, key, 'pet_warehouse')
            file = os.path.join(DATA_PATH, data['账号'], pid, 'pet_warehouse.json')
            dict2file(data, file)

    def save(self, key=None):
        """
        redis数据落盘
        :return:
        """
        from common.common import sprint
        if key:  # 指定key保存数据
            self.redis_save(key)
        else:  # 未指定key保存所有
            for key in self.conn.keys():
                self.redis_save(key)
        sprint('redis数据已保存')


if __name__ == '__main__':
    redis_sever = RedisServer()
    server.redis_server = redis_sever
    server.redis_server.setup()
    server.redis_server.start()
