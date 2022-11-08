import uuid
import json
from redis.client import Redis
import time


def send(sk, cmd: str, send_data: dict):
    """
    socket发送数据
    :param sk: socket
    :param cmd:
    :param send_data:
    :return:
    """
    send_data['cmd'] = cmd
    json_str = json.dumps(send_data)
    json_str_len = len(json_str)
    len_bytes = json_str_len.to_bytes(2, byteorder='big')
    send_bytes = len_bytes + json_str.encode(encoding='utf-8')
    try:
        sk.sendall(send_bytes)
    except:
        sprint('发送网络数据失败, 请尝试重新登陆')


def sprint(text: str, tp='info'):
    """
    系统打印
    :param text: 打印内容
    :param tp: 类型, info/warning/error
    :return:
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    t = time.gmtime()
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", t)
    if tp == 'info':
        color = OKGREEN
    elif tp == 'warning':
        color = WARNING
    else:
        color = FAIL
    print('{}[{}][{}] {}{}'.format(color, time_string, tp, text, ENDC))


def dict2file(data: dict, file: str):
    """
    将字典保存成json文件
    :param data:
    :param file:
    :return:
    """
    data_str = json.dumps(data, indent=4, ensure_ascii=False)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(data_str)


def file2dict(file) -> dict:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def redis_set_data(redis_client: Redis, key: str, data: dict):
    lock_value = str(uuid.uuid4())
    acquire_redis_lock(redis_client, lock_value)
    data_str = json.dumps(data)
    redis_client.set(key, data_str)
    release_redis_lock(redis_client, lock_value)


def redis_set_hash_data(redis_client: Redis, key: str, hash_value: str, data: dict):
    lock_value = str(uuid.uuid4())
    acquire_redis_lock(redis_client, lock_value)
    data_str = json.dumps(data)
    redis_client.hset(key, hash_value, data_str)
    release_redis_lock(redis_client, lock_value)


def redis_get_data(redis_client: Redis, key: str) -> dict:
    lock_value = str(uuid.uuid4())
    acquire_redis_lock(redis_client, lock_value)
    data_str = redis_client.get(key)
    if data_str:
        data = json.loads(data_str)
        release_redis_lock(redis_client, lock_value)
        return data
    else:
        release_redis_lock(redis_client, lock_value)
        return {}


def redis_get_hash_data(redis_client: Redis, key: str, hash_value: str) -> dict:
    lock_value = str(uuid.uuid4())
    acquire_redis_lock(redis_client, lock_value)
    data_str = redis_client.hget(key, hash_value)
    if data_str:
        data = json.loads(data_str)
        release_redis_lock(redis_client, lock_value)
        return data
    else:
        release_redis_lock(redis_client, lock_value)
        return {}


def acquire_redis_lock(redis_client: Redis, lock_value: str, timeout=2):
    # nx - 如果设置为True，则只有name不存在时，当前set操作才执行
    # ex - 过期时间（秒）
    while True:
        result = redis_client.set('lock', lock_value, nx=True, ex=timeout)
        if result:
            break


def release_redis_lock(redis_client: Redis, lock_value: str):
    cur_lock = redis_client.get('lock')
    # 保证只能解除自己设定的锁
    if cur_lock == lock_value:
        redis_client.delete('lock')
