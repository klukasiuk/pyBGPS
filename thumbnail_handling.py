from threading import Thread
import settings
import os
import Queue


class ThumbnailThread(Thread):

    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        client_id = self.sock.recv(settings.client_id_size)

        is_there_that_id = False

        for (thumb_id, send, to_send) in settings.thumbnail_receivers_list:
            if thumb_id == client_id:
                is_there_that_id = True
                break

        if not is_there_that_id:
            settings.thumbnail_receivers_list.append((client_id, [], Queue.Queue()))
            print "New thumbnails client : " + client_id

        thumbnails = os.listdir(settings.thumbnails_path)

        thumb_to_send = "dupa"

        for thumb_id, sent_thumb, to_send in settings.thumbnail_receivers_list:
            if thumb_id == client_id:
                for t in thumbnails:

                    is_new_thumb = True

                    for t_send in sent_thumb:
                        if t == t_send:
                            is_new_thumb = False

                    if is_new_thumb:
                        to_send.put(t)
                        sent_thumb.append(t)

                if to_send.empty():
                    self.sock.send(settings.no_thumb_msg)
                    self.sock.close()
                    return

                thumb_to_send = to_send.get()

                break

        filename = settings.thumbnails_path + "/" + thumb_to_send

        self.sock.send(thumb_to_send)

        with open(filename, 'rb') as f:
            file_data = f.read(settings.image_buffer_size)
            while file_data:
                self.sock.send(file_data)
                file_data = f.read(settings.image_buffer_size)
            f.close()

        self.sock.close()