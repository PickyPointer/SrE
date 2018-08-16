import json
import numpy as np
from twisted.internet.defer import inlineCallbacks, returnValue, DeferredLock
from twisted.internet.reactor import callLater, callInThread

from server_tools.device_server import Device
from lib.helpers import sleep

class Ldc80xxSerial(Device):
    """ thorlabs ldc80xx device 

    write to serial->GPIB adapter with write_to_slot and query with query_with_slot
    so that multiple instances of this device don't get confused responses
    from thr PRO8
    """
    serial_server_name = None
    serial_address = None
    serial_baudrate = 19200
    serial_timeout = 2.0

    pro8_slot = None

    current_ramp_duration = 5
    current_ramp_num_points = 10
    current_range = (0.0, 0.153)
    current_stepsize = 1e-4
    default_current = 0

    update_parameters = ['state', 'current', 'power']

    @inlineCallbacks
    def initialize(self):
        yield self.connect_labrad()
        self.serial_server = yield self.cxn[self.serial_server_name]
        yield self.serial_server.select_interface(self.serial_address)
        yield self.serial_server.disconnect()
        yield self.serial_server.select_interface(self.serial_address)
        yield self.serial_server.timeout(self.serial_timeout)
        yield self.serial_server.baudrate(self.serial_baudrate)
        yield self.get_parameters()
    
    @inlineCallbacks
    def get_parameters(self):
        self.state = yield self.get_state()
        self.current = yield self.get_current()
        self.power = yield self.get_power()

    @inlineCallbacks
    def write_to_slot(self, command):
        slot_command = ':SLOT {}\n'.format(self.pro8_slot)
        yield self.serial_server.write(slot_command)
        yield self.serial_server.write(command)
    
    @inlineCallbacks
    def query_to_slot(self, command):
        slot_command = ':SLOT {}\n'.format(self.pro8_slot)
        yield self.serial_server.write(slot_command)
        yield self.serial_server.write(command)
        ans = yield self.serial_server.read_line()
        print ans
        returnValue(ans)

    @inlineCallbacks
    def get_current(self):
        slot_command = ':SLOT {}\n'.format(self.pro8_slot)
        yield self.serial_server.write(slot_command)
        yield self.serial_server.write(':ILD:SET?\n')
        ans = yield self.serial_server.read_line() 
        print ans
        returnValue(float(ans[9:]))

    @inlineCallbacks
    def set_current(self, current):
        min_current = self.current_range[0]
        max_current = self.current_range[1]
        current = sorted([min_current, current, max_current])[1]
        command = ':ILD:SET {}\n'.format(current)
        
        yield self.write_to_slot(command)
        self.power = yield self.get_power()

    @inlineCallbacks
    def get_power(self):
        command = ':POPT:ACT?\n'
        ans = yield self.query_to_slot(command)
        print ans
        returnValue(float(ans[10:]))
    
    @inlineCallbacks
    def set_power(self, power):
        yield None

    @inlineCallbacks
    def get_state(self):
        command = ':LASER?\n'
        ans = yield self.query_to_slot(command)
        if ans == ':LASER ON':
            returnValue(True)
        elif ans == ':LASER OFF':
            returnValue(False)

    @inlineCallbacks
    def set_state(self, state):
        if state:
            command = ':LASER ON\n'
        else:
            command = ':LASER OFF\n'
        
        yield self.write_to_slot(command)

    @inlineCallbacks
    def dial_current(self, stop):
        start = yield self.get_current()
        currents = np.linspace(start, stop, self.current_ramp_num_points+1)[1:]
        dt = float(self.current_ramp_duration) / self.current_ramp_num_points
        for current in currents: 
            yield self.set_current(current)
            yield sleep(dt)
    
    @inlineCallbacks
    def warmup(self):
        yield None
        callInThread(self.do_warmup)
#        yield self.do_warmup()
    
    @inlineCallbacks
    def do_warmup(self):
        yield self.set_state(True)
        yield self.dial_current(self.default_current)
        yield sleep(.1)
        yield self.get_parameters()
        update = {self.name: {p: getattr(self, p) for p in self.update_parameters}}
        yield self.device_server.update(json.dumps(update))

    @inlineCallbacks
    def shutdown(self):
        yield None
        callInThread(self.do_shutdown)
#        yield self.do_shutdown()

    @inlineCallbacks
    def do_shutdown(self):
        yield self.dial_current(min(self.current_range))
        yield self.set_state(False)
        yield sleep(.1)
        yield self.get_parameters()
        update = {self.name: {p: getattr(self, p) for p in self.update_parameters}}
        yield self.device_server.update(json.dumps(update))
