import uuid
import json
from redis.client import Redis
import time
import os
import random
from common.socket_id import *
from common.constants import *


# class NPC:
#     def __init__(self):
#         self.npc_id = 0
#         self.npc_type = '普通'  # 0普通, 2商业, 3特殊, 4传送, 5任务
#         self.dialogue = {'contents': ['你找我有事吗?', '欢迎来到梦幻西游~'], 'options': ['随便看看']}
#
#     def talk(self, pid, option=None):
#         cont = random.sample(self.dialogue['contents'], 1)
#         op = self.dialogue['options']
#
#         send_data = {'npc_id': self.npc_id, '对话': cont, '选项': op, '类型': 'npc'}
#         send2pid(pid, S_发送NPC对话, send_data)


class NPC:
    def __init__(self, id) -> None:
        self.npc_id = id
        self.map_id = 0
        self.name = '未知'
        self.title = ''
        self.model = '泡泡'
        self.x, self.y = 0, 0
        self.direction = 0
        self.npc_type = '普通'
        self.contents = []
        self.options = []
        self.team_trigger = False

    def setup(self):
        """
        根据npc_id从excel加载数据
        :return:
        """
        my_npc_data = BH_NPC_DATA[self.npc_id]
        self.name = my_npc_data['名称']
        self.model = my_npc_data['模型']
        self.x = int(my_npc_data['X'])
        self.y = int(my_npc_data['Y'])
        self.direction = int(my_npc_data['方向'])
        self.npc_type = my_npc_data['事件']
        self.title = my_npc_data['称谓']
        self.contents = parse_cell(my_npc_data['对话'])
        self.options = parse_cell(my_npc_data['选项'])
        self.team_trigger = my_npc_data['队伍']
        self.map_id = my_npc_data['地图']

    def send(self, pid, contents: list = None, options: list = None):
        """
        NPC发送对话
        :param pid:
        :param contents:
        :param options:
        :return:
        """
        if contents:
            cont = contents
        else:
            cont = self.contents
        if options:
            op = options
        else:
            op = self.options

        send_data = {'npc_id': self.npc_id, '对话': cont, '选项': op, '类型': 'npc'}
        send2pid(pid, S_发送NPC对话, send_data)

    def response(self, pid, msg):
        """
        根据点选的msg回应
        :param pid:
        :param msg:
        :return:
        """
        pass


def get_players_in_scene(pid, map_id, include_self=False):
    """
    获取同地图的所有玩家pid
    :param pid:
    :param map_id:
    :param include_self: 是否包含自己
    :return:
    """
    if not map_id:
        map_id = rget(pid, CHAR, '地图')
    players = []
    for _pid in get_all_players():
        if int(_pid) != int(pid) and rget(_pid, CHAR, '地图') == map_id:
            players.append(_pid)
    if include_self:
        players.append(pid)

    return players


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
    len_bytes = json_str_len.to_bytes(4, byteorder='big')
    send_bytes = len_bytes + json_str.encode(encoding='utf-8')
    try:
        sk.sendall(send_bytes)
    except BaseException as e:
        print('发送网络数据失败:', str(e), cmd, send_data)


def send2gw(cmd: str, send_data: dict, flag=0):
    from common.server_process import server
    if flag == 0:
        send(server.game_server.socket, cmd, send_data)
    elif flag == 1:
        send(server.battle_server.socket, cmd, send_data)


def send2pid(pid, cmd: str, send_data: dict):
    send_data['pid'] = pid
    send2gw(cmd, send_data)


def send2pid_game_msg(pid, msg):
    """
    给玩家发送系统提示
    :param pid:
    :param msg:
    :return:
    """
    send2pid(pid, S_系统提示, dict(内容=msg))


def send2pid_hero_data(pid):
    send_data = rget(pid, CHAR)
    send2pid(pid, S_角色数据, send_data)


def send2pid_in_scene(pid, cmd, send_data, include_self=False):
    ids = get_players_in_scene(pid, None, include_self=include_self)
    for _id in ids:
        send2pid(_id, cmd, send_data)


def empty_indexed_dict(num: int):
    d = {}
    for i in range(num):
        d[i] = None
    return d


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
    将字典保存成json文件(先存临时文件)
    :param data:
    :param file:
    :return:
    """
    tmp_file = file + '_tmp'
    data_str = json.dumps(data, indent=4, ensure_ascii=False)
    with open(tmp_file, 'w', encoding='utf-8') as f:
        f.write(data_str)
    if os.path.exists(file):
        os.remove(file)
    os.rename(tmp_file, file)


def file2dict(file) -> dict:
    print('file2dict:', file)
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def redis_set_data(redis_client: Redis, key: str, data: dict):
    lock_value = str(uuid.uuid4())
    acquire_redis_lock(redis_client, lock_value)
    data_str = json.dumps(data, ensure_ascii=False)
    redis_client.set(key, data_str)
    release_redis_lock(redis_client, lock_value)


def redis_set_hash_data(redis_client: Redis, key: str, hash_value: str, data: dict):
    lock_value = str(uuid.uuid4())
    acquire_redis_lock(redis_client, lock_value)
    data_str = json.dumps(data, ensure_ascii=False)
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


def rget(pid, db, *args):
    from common.server_process import server
    if not db:
        return server.redis_conn.hgetall(pid)
    data = redis_get_hash_data(server.redis_conn, pid, db)
    if data:
        _path = ''  # 数据路径
        d = data.copy()  # 根据path获取到的数据
        for arg in args:
            _path = _path + '/' + str(arg)
            if arg in d:
                d = d[arg]
            else:
                # 数据路径不存在则警告
                sprint('rget error:{} {} {}'.format(pid, db, _path), 'warning')
                return None
        return d


def rset(pid, db, value, *args):
    """
    向redis写入数据, 先读出整个数据, 修改字典, 再写入redis
    :param pid: 玩家id
    :param db: 玩家数据库 char/pet/warehouse...
    :param value: 要设置的值
    :param args: 数据路径
    :return:
    """
    from common.server_process import server
    data = redis_get_hash_data(server.redis_conn, pid, db)
    if data:
        _path = ''  # 数据路径
        if args:
            args = [arg for arg in args]
            key = args[-1]
            args.pop(-1)
            for arg in args:
                _path = _path + '/' + str(arg)
                if arg in args:
                    data = data[arg]
                else:
                    # 数据路径不存在则警告
                    sprint('rget error:{} {} {}'.format(pid, db, _path), 'warning')
                    return None
            data[key] = value
            redis_set_hash_data(server.redis_conn, pid, db, data)
        else:
            redis_set_hash_data(server.redis_conn, pid, db, value)


def get_filenames_in_path(path):
    filenames = []
    if os.path.exists(path):
        for _, _, files in os.walk(path):
            for file in files:
                filenames.append(file)
    return filenames


def load_npc_objects():
    """
    从excel加载所有NPC对象
    :return:
    """
    from common.server_process import server
    for npc_id in BH_NPC_DATA.keys():
        npc = NPC(npc_id)
        npc.setup()
        server.npc_objects[npc_id] = npc


# 获取所有NPC
def import_npc_objects():
    """
    根据NPC脚本加载NPC
    :return:
    """
    files = get_filenames_in_path('scene/npc')
    # npc_importer.py是每次动态生成的
    with open('scene/npc/npc_importer.py', 'w', encoding='utf-8') as f:
        f.write('from common.server_process import server\n')
        for file in files:
            if not '__init__' in file and not 'npc_importer' in file and not '.pyc' in file and '.py' in file:
                f.write('from scene.npc.{} import npc\n'.format(file.rstrip('.py')))
                _str = 'server.npc_objects[\'{}\'] = {}'.format(file.rstrip('.py'), 'npc')
                f.write(_str + '\n')
    import scene.npc.npc_importer


def get_all_players() -> list:
    from common.server_process import server
    keys = server.redis_conn.keys()
    if 'lock' in keys:
        keys.remove('lock')
    return keys


def gdv(d, k):
    """
    Get dict value, 获取字典对应键的值
    若存在改键则返回值, 不存在则返回0
    """
    if k not in d:
        return 0
    else:
        return d[k]
