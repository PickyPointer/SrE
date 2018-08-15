from devices.ldc80xx.ldc80xxSerial import Ldc80xxSerial

class BlueMaster(Ldc80xxSerial):
    autostart = False
    serial_server_name = 'yeelmo_serial'
    serial_address = '/dev/ttyUSBblue_controller'

    pro8_slot = 7
    default_current = 0.1478

__device__ = BlueMaster
