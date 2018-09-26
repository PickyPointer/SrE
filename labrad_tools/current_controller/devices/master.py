from devices.ldc80xx.ldc80xxVXI11 import Ldc80xxVXI11

class BlueMaster(Ldc80xxVXI11):
    autostart = True
    vxi11_address = 'TCPIP::192.168.1.15::gpib0,10::INSTR'

    pro8_slot = 7
    default_current = 0.1478

__device__ = BlueMaster
