from collections import deque
from threading import Thread, Lock
import logging
import traceback
import sys
from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal



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

class QWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    def __init__(self, fn, *args, **kwargs):
        super(QWorker, self).__init__()
        self.fn = fn
        self.args=args
        self.kwargs = kwargs
        
    
    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.result.emit(result)
        finally:
            self.finished.emit()

