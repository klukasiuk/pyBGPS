from beacon import Beacon

# SETTINGS

verbose_mode = False

# server_ip = "89.74.10.90"
server_ip = "194.29.155.29"               					# Server local ip

server_image_in_port = 6000							        # Main server port
server_image_out_port = server_image_in_port + 1
server_telem_in_port = server_image_in_port + 2
server_telem_out_port = server_image_in_port + 3
server_cmd_in_port = server_image_in_port + 4
server_cmd_out_port = server_image_in_port + 5
server_thumb_out_port = server_image_in_port + 6
server_img_req_port = server_image_in_port + 7

client_id_size = 3
server_id = "SRV"
gcs_id = "GCS"

# Also set in client_data:
birdie_id = "BRD"
uav_one_id = "XD1"
uav_two_id = "XD2"
uav_three_id = "XD3"

image_buffer_size = 1024                                   # Size of buffer
image_name_size = 31                                     # Size of image name in bytes
image_request_size = 512
image_queue_warning_size = 100

telemetry_max_string_size = 512

command_max_string_size = 512

no_cmd_msg = "NO_COMMANDS_TO_SEND"
no_telem_msg = "NO_TELEMETRY_TO_SEND"
no_thumb_msg = "NO_THUMBNAIL_TO_SEND"
no_img_msg = "NO_IMG_TO_SEND"

# GLOBALS

images_path = "images"
thumbnails_path = "thumb"

sockets = []
threads = []

command_list = []

image_receivers_list = []
telemetry_receivers_list = []
thumbnail_receivers_list = []

# SQUARES VARIABLES
square_centers_file = "squares.txt"

# environmental constant
# one letter variable ??? seriously ?
n = 2

squares_matrix = []

beacon_list = [Beacon(1, 1, 0, 0, 0, 1),
               Beacon(2, 1, 0, 0, 0, 2),
               Beacon(2, 2, 0, 0, 0, 2),
               Beacon(3, 1, 0, 0, 0, 3),
               Beacon(3, 2, 0, 0, 0, 3),
               Beacon(3, 3, 0, 0, 0, 3),
               Beacon(4, 1, 0, 0, 0, 5),
               Beacon(4, 2, 0, 0, 0, 5),
               Beacon(4, 3, 0, 0, 0, 5),
               Beacon(4, 4, 0, 0, 0, 5)]
# each tupple: (major, minor, lat, lon, weights_sum, points)
