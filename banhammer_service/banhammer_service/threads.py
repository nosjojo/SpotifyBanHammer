from collections import deque
from threading import Thread, Lock
import logging


class Worker(Thread):
    def __init__(self, queue: deque, lock: Lock) -> None:
        super().__init__()
        self.queue = queue
        self.lock = lock
        self.logger = logging.getLogger("BanHammer")

    def run(self):
        fcn, *args = self.queue.popleft()
        self.lock.acquire()
        self.logger.debug(f"Executing {fcn} with {args}")
        fcn(*args)
        self.lock.release()
        return
