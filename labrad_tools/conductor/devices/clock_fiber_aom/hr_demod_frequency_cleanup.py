from twisted.internet.defer import inlineCallbacks
from labrad.wrappers import connectAsync

from conductor_device.conductor_parameter import ConductorParameter

class HrDemodFrequencyCleanup(ConductorParameter):
    priority = 1
    dark_frequency = 2.0*135.374e6

    @inlineCallbacks
    def initialize(self):
        yield self.connect()
        yield self.cxn.rf.select_device('cu_pulse')
        yield self.cxn.rf.frequency(self.dark_frequency)
        print 'hr_demod_frequency_cleanup init\'d with freq: {}'.format(self.dark_frequency)
    
    @inlineCallbacks
    def update(self):
        if self.value is not None:
            yield self.cxn.rf.frequency(value)
