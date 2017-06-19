from threading import Thread
import settings
import os


class ImageRequestThread(Thread):

    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        image_name = self.sock.recv(settings.image_name_size)

        files = os.listdir(settings.images_path)

        file_exist = False

        for f in files:
            if f == image_name:
                file_exist = True
                break

        if not file_exist:
            self.sock.send(settings.no_img_msg)
            self.sock.close()
            return

        image_name = settings.images_path + "/" + image_name

        with open(image_name, 'rb') as f:
            file_data = f.read(settings.image_buffer_size)
            while file_data:
                self.sock.send(file_data)
                file_data = f.read(settings.image_buffer_size)
            f.close()

        self.sock.close()
