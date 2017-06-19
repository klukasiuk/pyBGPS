import os
import time
from threading import Lock


class Logger:
    def __init__(self):
        self.logger_lock = Lock()

        self.write_to_console = False

        if not os.path.exists("logs"):
            os.makedirs("logs")

        date = time.strftime('%d.%m.%Y_%H.%M.%S')
        name = 'logs/log_' + date + ".txt"
        self.file = open(name, "w")
        os.chmod(name, 0666)

    def log_info(self, text):
        self.logger_lock.acquire()

        if self.write_to_console :
            print "Info : " + text

        self.file.write("Info : " + text)
        self.file.write("\n")

        self.logger_lock.release()

    def flush(self):
        self.logger_lock.acquire()

        self.file.flush()
        os.fsync(self.file.fileno())

        self.logger_lock.release()

    def close(self):
        self.file.close()

my_logger = Logger()
