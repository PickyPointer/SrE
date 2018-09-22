import json
import numpy as np

from server_tools.device_server import Device
from lib.helpers import sleep
import vxi11

class Ldc80xxVXI11(Device):
    """ thorlabs ldc80xxVXI11 device 

    write to gpib bus via Ethernet adapter with write_to_slot and query with query_with_slot
    so that multiple instances of this device don't get confused responses
    from thr PRO8
    """
    vxi11_address = None

    pro8_slot = None

    current_ramp_duration = 5
    current_ramp_num_points = 10
    current_range = (0.0, 0.153)
    current_stepsize = 1e-4
    default_current = 0

    update_parameters = ['state', 'current', 'power']

    def initialize(self):
        self.inst = vxi11.Instrument(self.vxi11_address)
        self.get_parameters()
    
    def get_parameters(self):
        self.state = self.get_state()
        self.current = self.get_current()
        self.power = self.get_power()

    def write_to_slot(self, command):
        slot_command = ':SLOT {};'.format(self.pro8_slot)
        self.inst.write(slot_command + command)
    
    def query_to_slot(self, command):
        slot_command = ':SLOT {};'.format(self.pro8_slot)
        ans = self.inst.ask(slot_command + command)
        return ans

    def get_current(self):
        command = ':ILD:SET?'
        ans = self.query_to_slot(command)
        return float(ans[9:])

    def set_current(self, current):
        min_current = self.current_range[0]
        max_current = self.current_range[1]
        current = sorted([min_current, current, max_current])[1]
        command = ':ILD:SET {}'.format(current)
        
        self.write_to_slot(command)
        self.power = self.get_power()

    def get_power(self):
        command = ':POPT:ACT?'
        ans = self.query_to_slot(command)
        return float(ans[10:])
    
    def set_power(self, power):
         return None

    def get_state(self):
        command = ':LASER?'
        ans = self.query_to_slot(command)
        if ans == ':LASER ON':
            return True
        elif ans == ':LASER OFF':
            return False

    def set_state(self, state):
        if state:
            command = ':LASER ON'
        else:
            command = ':LASER OFF'
        
        self.write_to_slot(command)

    def dial_current(self, stop):
        start = self.get_current()
        currents = np.linspace(start, stop, self.current_ramp_num_points+1)[1:]
        dt = float(self.current_ramp_duration) / self.current_ramp_num_points
        for current in currents: 
            self.set_current(current)
            sleep(dt)
    
    def warmup(self):
        callInThread(self.do_warmup)
#        yield self.do_warmup()
    
    def do_warmup(self):
        self.set_state(True)
        self.dial_current(self.default_current)
        sleep(.1)
        self.get_parameters()
        update = {self.name: {p: getattr(self, p) for p in self.update_parameters}}
        self.device_server.update(json.dumps(update))

    def shutdown(self):
        callInThread(self.do_shutdown)
#        yield self.do_shutdown()

    def do_shutdown(self):
        self.dial_current(min(self.current_range))
        self.set_state(False)
        sleep(.1)
        self.get_parameters()
        update = {self.name: {p: getattr(self, p) for p in self.update_parameters}}
        self.device_server.update(json.dumps(update))
