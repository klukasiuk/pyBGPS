from threading import Thread
import Queue
import settings


class ImageInThread(Thread):

    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        filename = self.sock.recv(settings.image_name_size)
        path = settings.images_path + "/" + filename

        with open(path, 'wb') as f:
            while True:
                data = self.sock.recv(settings.image_buffer_size)
                if not data:
                    f.close()
                    self.sock.close()
                    break
                f.write(data)

        for client_id, queue in settings.image_receivers_list:
            queue.put(path)

        if settings.verbose_mode:
            print "Image received"


class ImageOutThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock
        self.runFlag = False

    def run(self):
        client_id = self.sock.recv(settings.client_id_size)

        is_there_that_id = False

        for img_id, queue in settings.image_receivers_list:
            if img_id == client_id:
                is_there_that_id = True
                break

        if not is_there_that_id:
            settings.image_receivers_list.append((client_id, Queue.Queue()))
            print "New img client : " + client_id

        filename = ""

        for img_id, queue in settings.image_receivers_list:
            if img_id == client_id:
                if queue.empty():
                    self.sock.send(settings.no_img_msg)
                    self.sock.close()
                    return
                else:
                    filename = queue.get()
                break

        filename_send = filename[filename.find("/")+1:]

        self.sock.send(filename_send)

        with open(filename, 'rb') as f:
            file_data = f.read(settings.image_buffer_size)
            while file_data:
                self.sock.send(file_data)
                file_data = f.read(settings.image_buffer_size)
            f.close()

        self.sock.close()
