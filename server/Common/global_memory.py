from multiprocessing.shared_memory import SharedMemory
import json
from Common.constants import *


class GlobalMemory:
    def __init__(self):
        self.mem_blocks = []

    def create(self, data: dict):
        """
        创建角色数据共享内存空间, data: 玩家数据字典
        """
        data_bytes = json.dumps(data)
        mem_name = str(data['id'])
        if len(bytes) >= GLOBAL_MEM_SIZE:
            raise MemoryError('玩家数据长度超过限制![{}]'.format(mem_name))
        mem = SharedMemory(mem_name, create=True, size=GLOBAL_MEM_SIZE)
        mem.buf[0:len(bytes)] = data_bytes
        self.mem_blocks.append(mem)


gm = GlobalMemory()
