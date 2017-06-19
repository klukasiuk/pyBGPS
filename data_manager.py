import settings
import time
import Queue
import functions
import beacon_averager
import iteration
from threading import Thread


class DataManagerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mainFlag = True
        self.queue = Queue.Queue()

    def stop(self):
        self.mainFlag = False

    def run(self):

        while self.mainFlag:

            for cmd_id, cmd in settings.command_list:
                if cmd_id == settings.server_id:
                    print "Command received:\t" + cmd
                    command = cmd.split()
                    
                    if command[0] == "BAV":
                        command.pop(0)
                        functions.create_job_thread(beacon_averager.beacon_averager(command))

                    if command[0] == "DST":
                        command.pop(0)
                        functions.create_job_thread(iteration.store_kalman_data(command))

                    if command[0] == "CPL":
                        command.pop(0)
                        vehicle_id = command.pop(0)
                        msg = '\n'.join([str(bcn) for bcn in settings.beacon_list
                                         if bcn.lon != 0 and bcn.lat != 0 and bcn.last_seen_by == vehicle_id])
                        settings.command_list.append((vehicle_id, msg))

                    self.queue.put(cmd)
                    settings.command_list.remove((cmd_id, cmd))

            msg = '\n'.join([str(bcn) for bcn in settings.beacon_list if bcn.lon != 0 and bcn.lat != 0])

            if len(msg) > 1:
                for client_id, queue in settings.telemetry_receivers_list:
                    queue.put(msg)

            time.sleep(1)
