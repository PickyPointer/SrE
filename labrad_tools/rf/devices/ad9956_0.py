import devices.ad9956.ad9956
reload(devices.ad9956.ad9956)
from devices.ad9956.ad9956 import AD9956

class Channel(AD9956):
    autostart = True
    serial_server_name = "yeelmo_serial"
    serial_address = "/dev/ttyACM0"
    board_num = 0
    channel = 0

    default_frequency = 135.374e6 #Default fiber noise frequency

__device__ = Channel
