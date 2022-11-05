from multiprocessing import connection


def process_login(pipe: connection):
    while True:
        msg = pipe.recv()
        if msg:
            print('msg from gateway:', msg)