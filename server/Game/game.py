from Common.common import BaseServerProcess


class ProcessGame(BaseServerProcess):
    def __init__(self, lock):
        super(ProcessGame, self).__init__('GAME')
        self.lock = lock

    def run(self):
        self.lock.acquire()
        super(ProcessGame, self).run()
        self.lock.release()
        while True:
            pass