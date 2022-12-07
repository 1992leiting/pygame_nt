from common.constants import *
from common.common import *
import os
import json
from common.socket_id import *


def create_account(sk, account_name, passwd):
    """
    新建账户,先新建文件再读入redis
    :param sk: 客户端socket
    :param account_name: 账户名
    :param passwd: 账户密码
    :return:
    """
    account_path = DATA_PATH + str(account_name)
    account_config_file = account_path + '/account_config.json'
    if os.path.exists(account_path):
        send(sk, S_系统提示, dict(内容='账号已存在,无法继续创建'))
        sprint('账号已存在,无法继续创建!', 'warning')
        return
    os.mkdir(account_path)
    config = {'password': passwd, 'pid': []}
    with open(account_config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f)

    send(sk, S_系统提示, dict(内容='账号创建成功'))
    sprint('账号已创建:{}'.format(account_name))


def account_login(sk, account, passwd) -> bool:
    """
    账号登陆, 返回是否成功
    :param sk:
    :param account:
    :param passwd:
    :return: True/False
    """
    # 验证密码
    account_path = os.path.join(DATA_PATH, account)
    if not os.path.exists(account_path):
        send(server.tmp_client_socket[account], S_系统提示, dict(内容='账号不存在!'))
        return False
    account_config_file = os.path.join(DATA_PATH, account, 'account_config.json')
    account_config_data = file2dict(account_config_file)
    if not str(passwd) == str(account_config_data['password']):
        send(server.tmp_client_socket[account], S_系统提示, dict(内容='账号/密码错误!'))
        return False
    else:
        # 发送所有角色数据
        send_hero_data_by_account(sk, account)
        # 发送所有NPC数据
        # send(server.tmp_client_socket[account], S_所有NPC数据, dict(内容=NPCS))
        send(sk, S_所有NPC数据, dict(内容=BH_NPC_DATA))
        return True


def get_hero_data_by_pid(account, pid):
    """
    单独获取该账户下某一个id的人物数据
    :param account:
    :param pid:
    :return:
    """
    data_file_path = os.path.join(DATA_PATH, account, str(pid), 'char.json')
    hero_data = file2dict(data_file_path)
    return hero_data


def send_hero_data_by_account(sk, account):
    """
    登陆时, 发送这个账号所有的人物数据
    :param sk:
    :param account:
    :return:
    """
    heroes = []
    account_path = os.path.join(DATA_PATH, account)
    account_config_file = os.path.join(account_path, 'account_config.json')
    account_pids = file2dict(account_config_file)['pid']
    for pid in account_pids:
        heroes.append(get_hero_data_by_pid(account, pid))
    send(sk, S_账号所有人物, dict(内容=heroes, 账号=account))
