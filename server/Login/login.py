from Common.common import BaseServerProcess


class ProcessLogin(BaseServerProcess):
    def __init__(self, lock):
        super(ProcessLogin, self).__init__('LOGIN')
        self.lock = lock

    def run(self):
        self.lock.acquire()
        super(ProcessLogin, self).run()
        self.lock.release()
        while True:
            pass
