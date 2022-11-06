from Common.common import BaseServerProcess


class ProcessChat(BaseServerProcess):
    def __init__(self, lock):
        super(ProcessChat, self).__init__('CHAT')
        self.lock = lock

    def run(self):
        self.lock.acquire()
        super(ProcessChat, self).run()
        self.lock.release()
        while True:
            pass