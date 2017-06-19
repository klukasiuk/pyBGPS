from threading import Thread
import settings


class JobThread(Thread):
    def __init__(self, job):
        Thread.__init__(self)
        self.job = job

    def run(self):
        if self.job is not None:
            self.job()


def create_job_thread(func):

    new_job_thread = JobThread(func)
    new_job_thread.start()
    settings.threads.append(new_job_thread)
