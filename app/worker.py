from rq import Worker, Queue, Connection
from app import redis_conn
LISTEN = ['default']

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, LISTEN)))
        worker.work()
