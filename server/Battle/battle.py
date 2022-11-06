from Common.common import BaseServerProcess


class ProcessBattle(BaseServerProcess):
    def __init__(self, lock):
        super(ProcessBattle, self).__init__('BATTLE')
        self.lock = lock

    def run(self):
        self.lock.acquire()
        super(ProcessBattle, self).run()
        self.lock.release()
        while True:
            pass