from devices.ldc80xx.ldc80xxSerial import Ldc80xxSerial

class BlueTC(Ldc80xxSerial):
    autostart = False
    serial_server_name = 'yeelmo_serial'
    serial_address = '/dev/ttyUSBblue_controller'

    pro8_slot = 5
    default_current = 0.150

__device__ = BlueTC
