
import devices.sg382.sg382
reload(devices.sg382.sg382)
from devices.sg382.sg382 import SG382

class CUPulse(SG382):
    autostart = True
    vxi11_address='192.168.1.14'

    default_frequency = 2.0*135.374e6 #Default fiber noise demod freq
    frequency_range = (1e-6, 500e6)

__device__ = CUPulse


