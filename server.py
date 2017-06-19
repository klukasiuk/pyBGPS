# server.py

import socket
import os
import select
from data_manager import DataManagerThread
from image_handling import ImageInThread
from image_handling import ImageOutThread
from telemetry_handling import TelemetryInThread
from telemetry_handling import TelemetryOutThread
from command_handling import CommandInThread
from command_handling import CommandOutThread
from thumbnail_handling import ThumbnailThread
from image_request_handling import ImageRequestThread
import settings
import square
from logger import my_logger as logger

socket_image_in = None
socket_image_out = None
socket_telem_in = None
socket_telem_out = None
socket_cmd_in = None
socket_cmd_out = None
socket_thumb_out = None
socket_img_req = None


def initialize_server_sockets():
    global socket_image_in
    global socket_image_out
    global socket_telem_in
    global socket_telem_out
    global socket_cmd_in
    global socket_cmd_out
    global socket_thumb_out
    global socket_img_req

    socket_image_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_image_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_image_in.bind((settings.server_ip, settings.server_image_in_port))
    socket_image_in.listen(5)

    socket_image_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_image_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_image_out.bind((settings.server_ip, settings.server_image_out_port))
    socket_image_out.listen(5)

    socket_telem_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_telem_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_telem_in.bind((settings.server_ip, settings.server_telem_in_port))
    socket_telem_in.listen(5)

    socket_telem_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_telem_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_telem_out.bind((settings.server_ip, settings.server_telem_out_port))
    socket_telem_out.listen(5)

    socket_cmd_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cmd_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_cmd_in.bind((settings.server_ip, settings.server_cmd_in_port))
    socket_cmd_in.listen(5)

    socket_cmd_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cmd_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_cmd_out.bind((settings.server_ip, settings.server_cmd_out_port))
    socket_cmd_out.listen(5)

    socket_thumb_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_thumb_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_thumb_out.bind((settings.server_ip, settings.server_thumb_out_port))
    socket_thumb_out.listen(5)

    socket_img_req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_img_req.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_img_req.bind((settings.server_ip, settings.server_img_req_port))
    socket_img_req.listen(5)

    settings.sockets.append(socket_image_in)
    settings.sockets.append(socket_image_out)
    settings.sockets.append(socket_telem_in)
    settings.sockets.append(socket_telem_out)
    settings.sockets.append(socket_cmd_in)
    settings.sockets.append(socket_cmd_out)
    settings.sockets.append(socket_thumb_out)
    settings.sockets.append(socket_img_req)


def init_squares():
    input_file = open(settings.square_centers_file, 'r')
    for index, line in enumerate(input_file):
        if index == 0:  # First line contains dimensions of rectangle in squares
            # size_text = line.split()
            # lon_size = int(size_text[0])
            # lat_size = int(size_text[1])
            continue

        line_text = line.split()
        # number = int(line_text[0])
        lon = float(line_text[1])
        lat = float(line_text[2])
        sqr = square.Square(lon, lat)
        settings.squares_matrix.append(sqr)


def init_data_manager():
    data_manager = DataManagerThread()
    data_manager.start()
    settings.threads.append(data_manager)


def init_server():
    if not os.path.exists(settings.images_path):
        os.makedirs(settings.images_path)

    initialize_server_sockets()

    init_data_manager()

    init_squares()

    logger.log_info('Server initialized')
    print "Server initialized :)\n"


def close_server():
    print "\n CLOSING SERVER"

    for t in settings.threads:
        if hasattr(t, "stop"):
            t.stop()
        else:
            t.join()

    logger.flush()
    logger.close()


def main():

    init_server()

    while True:
        read, write, error = select.select(settings.sockets, settings.sockets, settings.sockets)

        for read_connection in read:
                if read_connection == socket_image_in:
                    (conn, (ip, port)) = read_connection.accept()

                    logger.log_info("Received image " + str(ip) + "," + str(port))

                    if settings.verbose_mode:
                        print "\nGot new img"

                    newthread = ImageInThread(conn)
                    newthread.start()
                    settings.threads.append(newthread)

                if read_connection == socket_image_out:
                    (conn, (ip, port)) = read_connection.accept()

                    logger.log_info("Received image request " + str(ip) + "," + str(port))

                    if settings.verbose_mode:
                        print "\nGot new img request"

                    newthread = ImageOutThread(conn)
                    newthread.start()
                    settings.threads.append(newthread)

                if read_connection == socket_telem_in:
                    (conn, (ip, port)) = read_connection.accept()

                    logger.log_info("Received telemetry data " + str(ip) + "," + str(port))

                    if settings.verbose_mode:
                        print "\nGot new telem"

                    newthread = TelemetryInThread(conn)
                    newthread.start()
                    settings.threads.append(newthread)

                if read_connection == socket_telem_out:
                    (conn, (ip, port)) = read_connection.accept()

                    logger.log_info("Received telemetry data request " + str(ip) + "," + str(port))

                    if settings.verbose_mode:
                        print "\nGot new telem request"

                    newthread = TelemetryOutThread(conn)
                    newthread.start()
                    settings.threads.append(newthread)

                if read_connection == socket_cmd_in:
                    (conn, (ip, port)) = read_connection.accept()

                    logger.log_info("Received command " + str(ip) + "," + str(port))

                    if settings.verbose_mode:
                        print "\nGot new cmd"

                    newthread = CommandInThread(conn)
                    newthread.start()
                    settings.threads.append(newthread)

                if read_connection == socket_cmd_out:
                    (conn, (ip, port)) = read_connection.accept()

                    logger.log_info("Received command request " + str(ip) + "," + str(port))

                    if settings.verbose_mode:
                        print "\nGot new cmd request"

                    newthread = CommandOutThread(conn)
                    newthread.start()
                    settings.threads.append(newthread)

                if read_connection == socket_thumb_out:
                    (conn, (ip, port)) = read_connection.accept()

                    logger.log_info("Received thumbnail request " + str(ip) + "," + str(port))

                    if settings.verbose_mode:
                        print "\nGot new thumb req"

                    newthread = ThumbnailThread(conn)
                    newthread.start()
                    settings.threads.append(newthread)

                if read_connection == socket_img_req:
                    (conn, (ip, port)) = read_connection.accept()

                    logger.log_info("Received image name request " + str(ip) + "," + str(port))

                    if settings.verbose_mode:
                        print "\nGot new img name request"

                    newthread = ImageRequestThread(conn)
                    newthread.start()
                    settings.threads.append(newthread)


# ENTRY POINT
try:
    main()
except KeyboardInterrupt, SystemExit:
    close_server()
    exit()
