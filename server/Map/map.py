from Common.common import BaseServerProcess


class ProcessMap(BaseServerProcess):
    def __init__(self, lock):
        super(ProcessMap, self).__init__('MAP')
        self.lock = lock

    def run(self):
        self.lock.acquire()
        super(ProcessMap, self).run()
        self.lock.release()
        while True:
            pass