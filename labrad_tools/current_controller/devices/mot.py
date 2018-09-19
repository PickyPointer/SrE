from devices.ldc80xx.ldc80xxVXI11 import Ldc80xxVXI11

class BlueMOT(Ldc80xxVXI11):
    autostart = False
    vxi11_address = 'TCPIP::192.168.1.15::gpib0,10::INSTR'

    pro8_slot = 4
    default_current = 0.1495

__device__ = BlueMOT
