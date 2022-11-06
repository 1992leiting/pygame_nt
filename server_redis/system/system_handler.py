from common.constants import *
from common.common import *
import os
import json


def create_account(account_name, passwd):
    """
    新建账户,先新建文件再读入redis
    :param account_name: 账户名
    :param passwd: 账户密码
    :return:
    """
    account_path = DATA_PATH + str(account_name)
    account_config_file = account_path + '/account_config.json'
    if os.path.exists(account_path):
        sprint('账号已存在,无法继续创建!', 'warning')
        return
    os.mkdir(account_path)
    config = {'password': passwd}
    with open(account_config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    sprint('账号已创建:{}'.format(account_name))

