# Author: Jacob Scott
# For use with yesr_analog_board_v2.py

# Force the length of a "bitfield". 
#Will add '0's to msb if under length or remove the msb if over length.
def force_len(bitlist, length):
	while len(bitlist) < length:
		bitlist.insert(0,0)
	while len(bitlist) > length:
		bitlist.pop(0)
	return bitlist

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
# 32-bit time step count and 18 bit voltage step loaded into ram as a 50 bit number.
class VoltagePoint:

	def __init__(self):
		self.VoltagePoint = (0, 0)
	# timeStepCount: number of 1us time steps for voltage incrementation.
	# voltageStep: voltage incrementation for each step. Note: 18 bit signed integer. Each integer corresponds to approx 0.0763 mV. 
	def __init__(self, timeStepCount, voltageStep):
		self.voltagePoint = (timeStepCount, voltageStep)
	
	# Overriden operator which includes a command number for reference.
	def __init__(self, timeStepCount, voltageStep, cmdNum):
		self.voltagePoint = (timeStepCount, voltageStep)
		self.cmdNum = cmdNum

	# Returns bit data to be inputted into fpga ram.
	def getBitList(self):
	
		# Get time bits and convert to correct length
		timeBits = bitfield(self.voltagePoint[0])
		force_len(timeBits, 32)
		
		# Get voltage bits and convert to correct length
		if self.voltagePoint[0] == 0:
			voltageBits = bitfield(self.voltagePoint[1])
		else:
			voltageBits = bitfieldTC(self.voltagePoint[1], 18)
		force_len(voltageBits, 18)
		
		# Combine timeBits and voltageBits and return for fpga input.
		voltagePointBits = timeBits
		voltagePointBits.extend(voltageBits)
		return voltagePointBits
		
	# Retruns the command number inputted at initialization.
	def getcmdNum(self):
		return self.cmdNum
	

# This class contains a List of VoltagePoint objects that describe the waveform that the dac will make.
class Waveform:		
	END_CMD = 0				# Command to end waveform normally.
	END_ALL_CMD = 3			# Command to end all waveforms on FPGA (once the fpga reaches this point)
	REPEAT_FOREVER_CMD = 1	# Command to repeat forever (until new trigger or end_all command is reached somewhere else)
	START_REPEAT_CMD = 2	# Command for repeat count return to point.
	REPEAT_COUNT_CMD = 4	# Command for repeating a specified number of times, then resuming to next command. Will repeat to most recent start_repeat_cmd.
	
	def __init__(self, channel):
		self.channel = channel
		self.initVoltage = 0
		self.error = False
		self.waveform = []
		
	# Assign initial voltage.
	def setInitialVoltage(self, iv):
		self.initVoltage = iv
	
	# Create and append a voltage point using total change of time (dt) and voltage step (dv):
	def newVoltagePoint(self, dt, dv):
		voltage_step = ramp_rate(dv, dt, 18)
		self.waveform.append(VoltagePoint(dt,voltage_step, len(self.waveform))
	
	# Add final command to waveform to signal end of waveform. 
	# cmd = 0: end (normal)
	# cmd = 1: repeat indefinitely
	# cmd = 2: start repeat flag
	# cmd = 3: end all
	# cmd = 4: repeat for finite number of times (requires repeat_ct to specify number of repititions)
	def specialCommand(self, cmd, repeat_ct = 0):
		if cmd <= 3:
			self.waveform.append(VoltagePoint(0, cmd, len(self.waveform)))
		elif cmd = 4:
			remDat = int(voltageCmd[1:len(voltageCmd)])
			datBits = bitfield(remDat)
			force_len(datBits, 18)
			datBits[0] = 1
			repeat_cmd = shifting(datBits)
			self.waveform.append(VoltagePoint(0, repeat_cmd, len(self.waveform)))
			
	# Number of voltage points
	def length(self):
		return len(self.waveform)
	
	# Returns the initial voltage data as bits of the waveform.
	def getInitVoltageBits(self):
		initVoltageBits = bitfieldTC(self.initVoltage, 18)
		force_len(initVoltageBits, 18)
		return initVoltageBits
	
	# Returns a list of bit lists for the voltage characteristics.
	def getWaveBitList(self):
		waveBitList = []
		for vp in self.waveform:
			waveBitList.append(vp.getBitList())
		return waveBitList
		
	def generateBytearray(self):
		ba = bytearray()
		for vp in self.waveform:
			bitlist = vp.getBitList()
			ba.append(chr(0)) 						# Most significant byte (always 0 because there are only 50 bits).
			ba.append(chr(shifting(bitlist[:-48])))
			ba.append(chr(shifting(bitlist[-48:-40])))
			ba.append(chr(shifting(bitlist[-40:-32])))
			ba.append(chr(shifting(bitlist[-32:-24])))
			ba.append(chr(shifting(bitlist[-24:-16])))
			ba.append(chr(shifting(bitlist[-16:-8])))
			ba.append(chr(shifting(bitlist[-8:])))	# Least significant byte
		return ba
	
	# Get the waveform (voltagePoint array)
	def getWaveform(self):
		return self.waveform
