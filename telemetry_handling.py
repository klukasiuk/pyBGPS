import settings
from threading import Thread
import Queue


class TelemetryInThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        telemetry_string = self.sock.recv(settings.telemetry_max_string_size)

        for client_id, queue in settings.telemetry_receivers_list:
            queue.put(telemetry_string)

        print "Telemetry received : " + telemetry_string

        self.sock.close()


class TelemetryOutThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):

        client_id = self.sock.recv(settings.client_id_size)

        is_there_that_id = False

        for telem_id, queue in settings.telemetry_receivers_list:
            if telem_id == client_id:
                is_there_that_id = True
                break

        if not is_there_that_id:
            settings.telemetry_receivers_list.append((client_id, Queue.Queue()))
            print "New telemetry client : " + client_id

        telemetry_string = ""

        for telem_id, queue in settings.telemetry_receivers_list:
            if telem_id == client_id:
                if queue.empty():
                    telemetry_string = settings.no_telem_msg
                else:
                    telemetry_string = queue.get()
                break

        self.sock.send(telemetry_string)

        self.sock.close()
