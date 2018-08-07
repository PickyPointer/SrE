import json
import waveform

from twisted.internet.defer import inlineCallbacks, returnValue

from server_tools.device_server import Device
from lib.analog_ramps import RampMaker
from lib.helpers import time_to_ticks
from lib.helpers import voltage_to_signed
from lib.helpers import voltage_to_unsigned
from lib.helpers import ramp_rate

T_WAIT_TRIG = 42.94967294
#------------Some tools for DAC control-------------------
# Get the state wire values to be inputted into the FPGA.
def getStateValue(state):
	return {
		'idle' : [0,0],
		'load' : [0,1],
		'ready': [1,0]
		}.get(state)
		def bitfieldTC(n, prec):
	return [1 if digit=='1' else 0 for digit in bin(n % (1<<prec))[2:]]
	
# Convert unsigned integer (will take absolute value) to binary.
def bitfield(n):
	return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

# Convert Integer to two's compliment at a number of bits.
def twos_comp(val, bits):
	"""compute the 2's complement of int value val"""
	if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
		val = val - (1 << bits)		# compute negative value
	return val						 # return positive value as is

# Convert unsigned bit list to integer.	
def shifting(bitlist):
	out = 0
	for bit in bitlist:
		out = (out << 1) | bit
	return out
	
# Convert the 50 bit bitfield to a bytearray
def make_bytearray(bitfield):
	b4 = '{:04x}'.format(shifting(bitfield[34:50]))
	b3 = '{:04x}'.format(shifting(bitfield[18:34]))
	b2 = '{:04x}'.format(shifting(bitfield[2:18]))
	b1 = '{:04x}'.format(shifting(bitfield[0:2]))
	ba = bytearray(b1+b2+b3+b4)
	return ba
	
# Force the length of a "bitfield". 
#Will add '0's to msb if under length or remove the msb if over length.
def force_len(bitlist, length):
	while len(bitlist) < length:
		bitlist.insert(0,0)
	while len(bitlist) > length:
		bitlist.pop(0)
	return bitlist


class YeSrAnalogBoard(Device):
    sequencer_type = 'analog'

    okfpga_server_name = None
    okfpga_device_id = None
    
    channels = None

    bitfile = 'dac_fpga_bitstream.bit'

    mode_ints = {'idle': 0, 'load': 1, 'run': 2}
    mode_wire = 0x00
    sequence_pipe = 0x80
    channel_mode_wire = 0x09
    manual_voltage_wires = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
    clk = 48e6 / (8.*2. + 2.)
    mode = 'idle'

    sequence_bytes = []

    @inlineCallbacks
    def initialize(self):
        self.mode = 'idle'
        assert len(self.channels) ==  8
        for channel in self.channels:
            channel.set_board(self)

        yield self.connect_labrad()
        self.okfpga_server = yield self.cxn[self.okfpga_server_name]
        yield self.okfpga_server.select_interface(self.okfpga_device_id)

        yield self.okfpga_server.program_bitfile(self.bitfile)
        yield self.write_channel_modes()
        yield self.write_channel_manual_outputs()

    @inlineCallbacks
    def set_mode(self, mode):
        mode_int = self.mode_ints[mode]
        yield self.okfpga_server.set_wire_in(self.mode_wire, mode_int)
        yield self.okfpga_server.update_wire_ins()
        self.mode = mode

    @inlineCallbacks
    def program_sequence(self, sequence):
        waveforms = self.make_sequence_waveform(sequence)
        yield self.set_mode('load')
		for waveform in waveforms:
			data = waveform.generateBytearray()
			
		yield self.set_mode('idle')

    @inlineCallbacks
    def start_sequence(self):
        yield self.set_mode('run')

    def make_sequence_waveform(self, sequence):
        """ 
        take readable {channel: [{}]} to programmable [ramp_rate[16], duration[32]] + ...
        """

        for channel in self.channels:
            assert channel.key in sequence
            channel_sequence = sequence[channel.key]
            vf = channel_sequence[-1]['vf']
            channel_sequence.append({'dt': 10, 'type': 'lin', 'vf': vf})

            # uncommenting for quto-trigger
            channel_sequence = [cs for cs in channel_sequence if cs['dt'] < T_WAIT_TRIG]

            try:
                channel.set_sequence(channel_sequence)
            except:
                print channel.name
                print channel_sequence

        waveforms = []
        for channel in self.channels:
			waveform = Waveform(channel)
            for ramp in channel.sequence:
                vi_bits = voltage_to_signed(ramp['vi'])
                vf_bits = voltage_to_signed(ramp['vf'])
                dv_bits = vf_bits - vi_bits

                ti_ticks = time_to_ticks(self.clk, ramp['ti'])
                tf_ticks = time_to_ticks(self.clk, ramp['tf'])
                dt_ticks = tf_ticks - ti_ticks

				waveform.newVoltagePoint(dt, dv)
			waveform.specialCommand(0, Waveform.END_CMD)
			waveforms.append(waveform)
        return waveforms
    
    @inlineCallbacks
    def write_channel_modes(self):
        cm_list = [c.mode for c in self.channels]
        value = sum([2**j for j, m in enumerate(cm_list) if m == 'manual'])
        yield self.okfpga_server.set_wire_in(self.channel_mode_wire, value)
        yield self.okfpga_server.update_wire_ins()
    
    @inlineCallbacks
    def write_channel_manual_outputs(self): 
        for c, w in zip(self.channels, self.manual_voltage_wires):
            v = voltage_to_unsigned(c.manual_output)
            yield self.okfpga_server.set_wire_in(w, v)
        yield self.okfpga_server.update_wire_ins()
