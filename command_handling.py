import settings
from threading import Thread


class CommandInThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        command_string = self.sock.recv(settings.command_max_string_size)

        cmd_id = command_string[0:settings.client_id_size]
        cmd = command_string[settings.client_id_size:]

        settings.command_list.append((cmd_id, cmd))

        self.sock.close()


class CommandOutThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        client_id = self.sock.recv(settings.client_id_size)

        for cmd_id, cmd in settings.command_list:
            if cmd_id == client_id:
                self.sock.send(cmd)
                self.sock.close()
                settings.command_list.remove((cmd_id, cmd))
                return

        self.sock.send(settings.no_cmd_msg)
        self.sock.close()
