from common.common import *
from common.constants import *
from common.socket_id import *


class Battle:
    def __init__(self):
        self.battle_id = 0
        self.uuid = ''
        self.team0 = empty_20.copy()
        self.team1 = empty_20.copy()
