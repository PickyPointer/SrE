# Jacob Scott
# Octa-DAC, 18 bit, FPGA controlled, driver
# This program controls the fpga. It loads voltage data into the fpga ram and sets up dacs.

#Import opal kelly frontpanel API:
import ok
import time
import sys
import thread
import os
import numpy as np
import timeit

from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT, QObject, pyqtSignal
from multiprocessing import Lock

# MATH METHODS/TOOLS ##############################################################
def getStateValue(state):
	return {
		'idle' : [0,0],
		'load' : [0,1],
		'ready': [1,0]
		}.get(state)
# Return board model from given device ID.
def getDeviceModelFromID(id):
	return {
		0 : "Unknown",
		1 : "XEM3001v1",
		2 : "XEM3001v2",
		3 : "XEM3010",
		4 : "XEM3005",
		5 : "XEM3001CL",
		6 : "XEM3020",
		7 : "XEM3050",
		8 : "XEM9002",
		9 : "XEM3001RB",
		10 : "XEM5010",
		11 : "XEM6110LX45",
		12 : "XEM6110LX150",
		13 : "XEM6001",
		14 : "XEM6010LX45",
		15 : "XEM6010LX150",
		16 : "XEM6006LX9",
		17 : "XEM6006LX16",
		18 : "XEM6006LX25",
		19 : "XEM5010LX110",
		20 : "ZEM4310",
		21 : "XEM6310LX45",
		22 : "XEM6310LX150",
		23 : "XEM6110v2LX45",
		24 : "XEM6110v2LX150",
		25 : "XEM6002LX9",
		26 : "XEM6310MTLX45T",
		27 : "XEM6320LX130T",
		28 : "XEM7350K70T",
		29 : "XEM7350K160T",
		30 : "XEM7350K410T",
		31 : "XEM6310MTLX150T",
		32 : "ZEM5305A2",
		33 : "ZEM5305A7",
		34 : "XEM7001A15",
		35 : "XEM7001A35",
		36 : "XEM7360K160T",
		37 : "XEM7360K410T",
		38 : "ZEM5310A4",
		39 : "ZEM5310A7",
		40 : "ZEM5370A5",
		41 : "XEM7010A50",
		42 : "XEM7010A200",
		43 : "XEM7310A75",
		44 : "XEM7310A200"}.get(id,0)
# Convert integer to binary with prec number of digits: NOTE: Used Two's Compliment.
def bitfieldTC(n, prec):
	return [1 if digit=='1' else 0 for digit in bin(n % (1<<prec))[2:]]
	
# Convert unsigned integer (will take absolute value) to binary.
def bitfield(n):
	return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

def ramp_rate(bits, ticks, dac_bits=18):
	if ticks <= 0:
		message = 'time {} [s] corresponds to {} {} [Hz] clock cycles'.format(time, ticks, clk)
		raise Exception(message)
	signed_ramp_rate = int(bits * 2.0**int(np.log2(ticks) - 1.0) / ticks)
	if signed_ramp_rate > 0:
		return signed_ramp_rate
	else:
		return signed_ramp_rate + 2**dac_bits

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

# Generate a full byte array to load all 8 dacs using the waveform list "waveforms" parameter.	
def generateFullBytearray(waveforms):	
	if len(waveforms) == 8:
		ba = bytearray()
		ba.append(chr(0))
		ba.append(chr(shifting([0,0,0,0,0,1,0,0])))
		ba.append(chr(0))
		ba.append(chr(0))
		ba.append(chr(0))
		ba.append(chr(0))
		ba.append(chr(0))
		ba.append(chr(0))
		for i in range(0, 8):
			ba.append(chr(0))
		for wf in waveforms:
			for i in range(0,len(wf.waveform)):
				vp = wf.waveform[i]
				if i == (len(wf.waveform) - 1):
					a = 1
				else:
					a = 0
				bitlist = vp.getBitList()
				ba.append(chr(0)) 						# Most significant byte (always 0 because there are only 50 bits).
				ba.append(chr(shifting([a]+bitlist[:-48])))
				ba.append(chr(shifting(bitlist[-48:-40])))
				ba.append(chr(shifting(bitlist[-40:-32])))
				ba.append(chr(shifting(bitlist[-32:-24])))
				ba.append(chr(shifting(bitlist[-24:-16])))
				ba.append(chr(shifting(bitlist[-16:-8])))
				ba.append(chr(shifting(bitlist[-8:])))	# Least significant byte
			for i in range(0, 8):
				ba.append(chr(0))
		return ba
	else:
		return bytearray()
	
def force_len(bitlist, length):
	while len(bitlist) < length:
		bitlist.insert(0,0)
	while len(bitlist) > length:
		bitlist.pop(0)
	return bitlist
		
# OBJECTS/CONTROLLERS/CLASSES #####################################################

# 32-bit time step count and 18 bit voltage step loaded into ram as a 50 bit number.
class VoltagePoint:
	# timeStepCount: number of 1us time steps for voltage incrementation.
	# voltageStep: voltage incrementation for each step. Note: 18 bit signed integer. Each integer corresponds to approx 0.0763 mV. 
	def __init__(self, timeStepCount, voltageStep):
		self.voltagePoint = (timeStepCount, voltageStep)
	
	# Overriden operator which includes a command number for reference.
	def __init__(self, timeStepCount, voltageStep, cmdNum):
		self.voltagePoint = (timeStepCount, voltageStep)
		self.cmdNum = cmdNum

	# totalTimeStep: total time change (in micro seconds) for total voltage change in step. NOTE: same as timeStepCount in provious __init__.
	# totalVoltageStep: total voltage change in step.
	@classmethod
	def fromTotals(cls, totalTimeStep, totalVoltageStep):
		return cls(totalTimeStep, totalVoltageStep / totalTimeStep)

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
	

# This class contains a List of VoltagePoint objects that describe the waveform that the dac will take.
class Waveform:		
	def __init__(self, ctrl):
		self.ctrl = ctrl
		self.initVoltage = 0
		self.error = False
		self.waveform = []
	# Load data from csv and save as waveform data.
	def loadFromCSV(self, file):
		try:
			csvFile = open(file, "r")
			csvData = csvFile.readlines()
			timeData = 0
			voltageData = 0
			i = 0
			for csvLine in csvData:
				csvLine = csvLine.replace(' ', '')
				csvLine = csvLine.replace('\n', '')
				csvLineParsed = csvLine.split(',')
				voltage_rate = 0
				try:
					if i == 0:
						self.initVoltage = int(csvLineParsed[0])
						i += 1
						continue
					timeData = int(csvLineParsed[0])

					if timeData == 0:	# Check Command flag.
						voltageCmd = str(csvLineParsed[1].replace("\r",""))
						if voltageCmd[0] == 'r':	# Repeat command. All numbers following r specify number of repeats. Max: 17 bits (131071)
							remDat = int(voltageCmd[1:len(voltageCmd)])
							datBits = bitfield(remDat)
							force_len(datBits, 18)
							datBits[0] = 1
							voltage_rate = shifting(datBits)
						elif voltageCmd == "sr":	# Repeat start point. Default 0.
							voltage_rate = 2
						elif voltageCmd == "R":		# Total Repeat Command.
							voltage_rate = 1
						elif voltageCmd == "end":	# End this waveform (voltage remains what it is at)
							voltage_rate = 0
						elif voltageCmd == "endall":	# Set dac to prepare restart state. Allows for better restarting from trigger.
							voltage_rate = 3
					else:
						voltageData = int(csvLineParsed[1])
						voltage_rate = ramp_rate(voltageData, timeData)
				except:
					self.ctrl.log("Error on line {0} of csv file \"{1}\".".format(i + 1, file))
					self.error = True
					break
				vp = VoltagePoint(timeData, voltage_rate, i)
				self.waveform.append(vp)
				i += 1
		except:
			self.ctrl.log("Couldn't open file \"{0}\"".format(file))
			self.error = True
			
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

# This class handles all FPGA communications.
class FPGACom:
	BITFILE_NAME = '{0}/dac_fpga_bitstream.bit'.format(os.path.dirname(os.path.abspath(__file__)))
	# Initialization function. Established communication with FPGA.
	def __init__(self, ctrl):
		if len(sys.argv) > 1:
			try:
				self.BITFILE_NAME = '{0}/{1}'.format(os.path.dirname(os.path.abspath(__file__)), sys.argv[1])
			except:
				print("ERROR: Unkown Bitfile Name. Using default name.")
		self.lock = Lock()
		self.ctrl = ctrl
		self.wire0InputBits = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
		self.wire1InputBits = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
		self.cnt = 0;
	
	# Establishes a connection to the opal kelly device and sends pll configuration data. This function also initializes the dacs.
	def connect(self):
		self.device = ok.okCFrontPanel()
		devCount = 0
		devCount = self.device.GetDeviceCount()
		# Print out list to user for decision.
		self.ctrl.log("Which of the following is the DAC FPGA?")
		for i in range(devCount):
			self.ctrl.log("{0}: Device Model: {1}, Device Serial: {2}".format(i + 1, getDeviceModelFromID(self.device.GetDeviceListModel(i)), self.device.GetDeviceListSerial(i)))
		cont = True
		intChoice = 0
		# Make sure that the response is an integer within the correct range.
		while cont:
			cont = False
			self.ctrl.log("Enter an integer from 1 to {0}:".format(devCount))
			choice = self.ctrl.getUserInput()
			try:
				intChoice = int(choice)
			except ValueError:
				cont = True
				self.ctrl.log("Not an integer.")
			if (intChoice > devCount) or (intChoice < 1):
				self.ctrl.log("Out of Range")
				cont = True
		self.device.OpenBySerial(self.device.GetDeviceListSerial(intChoice - 1))
		self.device.ConfigureFPGA(self.BITFILE_NAME)
		
		if self.device.IsFrontPanelEnabled():
			self.ctrl.log("FrontPanel host interface enabled.")
			self.ctrl.enableGUI()
		else:
			self.ctrl.log("ERROR: FrontPanel host interface not detected.")
			return
		self.ctrl.enableGUI()
		pll22150 = ok.PLL22150()
		# Get the existing settings to modify them
		self.device.GetPLL22150Configuration(pll22150)
		 
		# Modify the PLL settings
		pll22150.SetReference(48.0, False)
		pll22150.SetVCOParameters(400, 48)
		pll22150.SetDiv1(ok.PLL22150.DivSrc_VCO, 400)
		pll22150.SetOutputSource(0, ok.PLL22150.ClkSrc_Div1ByN)
		pll22150.SetOutputEnable(0, True)
		
		# Output Current Settings
		self.ctrl.log("Details for pll:")
		self.ctrl.log("Reference: " + str(pll22150.GetReference()) + "\nVCO Freq: " + str(pll22150.GetVCOFrequency()))
		self.ctrl.log("Div1: " + str(pll22150.GetDiv1Divider()) + "\nSource: " + str(pll22150.GetDiv1Source()))
		self.ctrl.log("Output Freq: " + str(pll22150.GetOutputFrequency(0)) + "\nOutput Source: " + str(pll22150.GetOutputSource(0)))
		self.ctrl.log("VCO P: " + str(pll22150.GetVCOP()) + "\nVCO Q: "+ str(pll22150.GetVCOQ()) + '\n')
		
		# Save new settings to the device
		self.device.SetPLL22150Configuration(pll22150)
		self.device.EnableAsynchronousTransfers(True)
		
		self.setWire0InputBit(8, 0)
		self.setWire1InputBit(0, 0)
		self.updateIns()
		
		thread.start_new_thread(GUI.initAllDacListener, (self.ctrl.gui,))
		thread.start_new_thread(FPGACom.startShift, (self,))
		thread.start_new_thread(FPGACom.startFPChecker, (self,))
		self.setDacState('idle')
	
	# Repeatedly check if frontpanel interface is enabled.
	def startFPChecker(self):
		while True:
			self.lock.acquire()
			if self.device.IsFrontPanelEnabled() == False:
				self.ctrl.log("ERROR: FrontPanel host interface not detected.")
				self.ctrl.disableGUI()
				return
			self.lock.release()
			time.sleep(1)
			
	
	# Used for debug purposes. Control the data_shift signal's value through this program.
	def startShift(self):
		if self.cnt > 9:
			self.cnt = 9
			self.ctrl.log("New Shift Count Not Changed (9)")
		elif self.cnt < 0:
			self.cnt = 0
			self.ctrl.log("New Shift Count Not Changed (0)")
		else:
			self.ctrl.log("New Shift Count: {0}".format(self.cnt)) 
		newbits = bitfield(int(self.cnt))
		force_len(newbits, 4)
		bitlist = []
		force_len(bitlist, 16)
		bitlist[0] = newbits[0]
		bitlist[1] = newbits[1]
		bitlist[2] = newbits[2]
		bitlist[3] = newbits[3]
		self.device.SetWireInValue(0x01, shifting(bitlist))
		self.updateIns()
		
	
	# Set the dac to the inputted state. Setable states are 'idle', 'load', 'ready'.
	state = 'idle'
	def setDacState(self, state, do_update = True):
		self.state = state
		stateID = getStateValue(state)
		self.ctrl.log("DAC STATE: {0}".format(state))
		self.setWire0InputBit(11, stateID[0])
		self.setWire0InputBit(10, stateID[1])
		if do_update:
			self.device.UpdateWireIns()
		# self.setWire0InputBit(12, 1)
		# self.device.UpdateWireIns()
		# self.setWire0InputBit(12, 0)
		# self.device.UpdateWireIns()
		
	# Load a new set of RAM to dac. dac: integer from 0 to 7 for dac selection. waveformData: a Waveform object containing desired waveform data.
	def loadDACRAM(self, dac, waveformData):
		if dac == None:
			self.loadAllDACRAM([waveformData,waveformData,waveformData,waveformData,waveformData,waveformData,waveformData,waveformData])
			return
		self.lock.acquire()
		
		# self.setDacState('idle')
		self.setDacState('load', False)
		timestart = time.time()
		self.setWire1InputBit()
		for i in range(0,8):
			self.wire0InputBits[15 - i] = 0
		if (dac <= 7):
			self.wire0InputBits[15 - dac] = 1
		self.setWire0InputBit()
		self.device.UpdateWireIns()
		# Set initial voltage if non-zero
		if waveformData.initVoltage != 0:
			iv_data_bits = waveformData.getInitVoltageBits()
			self.setWire0InputBit(8, 1)
			self.device.SetWireInValue(0x00, shifting(iv_data_bits[-16:]))
			self.device.SetWireInValue(0x01, shifting(iv_data_bits[-18:-16]))
			self.device.UpdateWireIns()
			self.setWire0InputBit(8,0)
			self.device.UpdateWireIns()
		# Load Waveform
		self.ctrl.log("Loading Data:")
		vpByteArray = bytearray()
		vpByteArray = waveformData.generateBytearray()
		self.device.WriteToPipeIn(0x80, vpByteArray)
		timeend = time.time()
		# Clear DAC Selection
		for i in range(0,8):
			self.wire0InputBits[15 - i] = 0
		self.setWire0InputBit()
		self.setDacState('idle')
		self.ctrl.log("Done loading {0} commands in {1}ms!".format(waveformData.length(), (timeend - timestart)*1000))
		self.lock.release()
		
	def loadAllDACRAM(self, waveformList):
		self.lock.acquire()
		timestart = time.time()
		for i in range(0,8):
			waveformList[0].generateBytearray()
		timeend = time.time()
		self.ctrl.log("{}ms".format((timeend - timestart)*1000))
		timestart = time.time()
		# self.setDacState('idle')
		self.setDacState('load')
		# Load Waveform
		self.ctrl.log("Loading Data:")
		self.device.ActivateTriggerIn(0x41, 0)
		for dac in range(0, 8):
			wf = waveformList[dac]
			vpByteArray = bytearray()
			t1 = time.time()
			vpByteArray = wf.generateBytearray()
			self.device.WriteToPipeIn(0x80, vpByteArray)
			self.device.ActivateTriggerIn(0x41, 0)
			t2 = time.time()
		self.setDacState('idle')
		timeend = time.time()
		self.ctrl.log("Done loading {0} commands in {1}ms!".format(len(vpByteArray), (timeend - timestart)*1000))
		self.lock.release()
		
	# Updates an individual wire1 bit. Must call updateIns() afterwards.
	def setWire0InputBit(self, bit = None, newBit = None):
		if (bit != None or newBit != None):
			self.wire0InputBits[15 - bit] = newBit
		self.device.SetWireInValue(0x02, shifting(self.wire0InputBits))
		
	# Updates an individual wire1 bit. Must call updateIns() afterwards.
	def setWire1InputBit(self, bit = None, newBit = None):
		if bit != None or newBit != None:
			self.wire1InputBits[15 - bit] = newBit
		self.device.SetWireInValue(0x03, shifting(self.wire1InputBits))
	
	# Manually trigger the dac.
	def triggerDAC(self):
		self.lock.acquire()
		self.setDacState("ready")
		if self.ctrl.extMode == False:
			self.ctrl.log("Triggering all DACs")
			self.device.ActivateTriggerIn(0x40, 0)
		self.lock.release()
	
	# Loads new bit values into fpga.
	def updateIns(self):
		self.lock.acquire()
		self.device.UpdateWireIns()
		self.lock.release()
		
	# Initialize DAC's register memory settings.
	def setupDAC(self, dac, RBUF = 1, OPGND = 0, DACTRI = 0, Bin_2sc = 0, SDODIS = 1, LINCOMP = 12):
		self.lock.acquire()
		self.setWire0InputBit(15, 0)
		self.device.UpdateWireIns()
		# Set up dac selection.
		if dac <= 7:
			dacbits = bitfield(dac)
			while len(dacbits) < 3:
				dacbits.insert(0,0)
			self.wire1InputBits[15 - 3] = dacbits[2]
			self.wire1InputBits[15 - 4] = dacbits[1]
			self.wire1InputBits[15 - 5] = dacbits[0]
			self.setWire1InputBit()
			self.device.UpdateWireIns() 
		# Reboot selected DAC
		self.setWire0InputBit(13, 1)
		self.device.UpdateWireIns()
		self.setWire0InputBit(13, 0)
		self.device.UpdateWireIns()
		
		self.setWire0InputBit(14,0)
		self.device.UpdateWireIns()
		
		if LINCOMP <= 15:
			self.wire1InputBits[15 - 14 : 16 - 11] = bitfield(LINCOMP)
		self.wire1InputBits[15 - 10] = 1
		self.wire1InputBits[15 - 9] = 0
		self.wire1InputBits[15 - 8] = 0
		self.wire1InputBits[15 - 7] = 1
		self.wire1InputBits[15 - 6] = 1
		self.setWire1InputBit()
		self.device.UpdateWireIns()
		
		# Trigger
		self.setWire1InputBit( 2,1)
		self.device.UpdateWireIns()
		self.setWire0InputBit(13,1)
		self.device.UpdateWireIns()
		self.setWire0InputBit(13,0)
		self.device.UpdateWireIns()
		self.setWire1InputBit( 2,0)
		self.device.UpdateWireIns()
		
		# Set initial voltage to 0
		self.setWire0InputBit(14,1)
		self.device.UpdateWireIns()
		self.setWire1InputBit( 2,1)
		self.device.UpdateWireIns()
		self.setWire0InputBit(13,1)
		self.device.UpdateWireIns()
		self.setWire0InputBit(13,0)
		self.device.UpdateWireIns()
		self.setWire1InputBit( 2,0)
		self.device.UpdateWireIns()
		self.setWire0InputBit(14,0)
		self.device.UpdateWireIns()
		
		if LINCOMP <= 15:
			self.wire1InputBits[15 - 14 : 16 - 11] = bitfield(LINCOMP)
		self.wire1InputBits[15 - 10] = SDODIS
		self.wire1InputBits[15 - 9] = Bin_2sc
		self.wire1InputBits[15 - 8] = DACTRI
		self.wire1InputBits[15 - 7] = OPGND
		self.wire1InputBits[15 - 6] = RBUF
		self.setWire1InputBit()
		self.device.UpdateWireIns()
		
		# Trigger
		self.setWire1InputBit( 2,1)
		self.device.UpdateWireIns()
		self.setWire0InputBit(13,1)
		self.device.UpdateWireIns()
		self.setWire0InputBit(13,0)
		self.device.UpdateWireIns()
		self.setWire1InputBit( 2,0)
		self.device.UpdateWireIns()
		
		self.setDacState("idle")
		self.lock.release()
		
# This class controls the GUI.
class GUI(QObject):
	addText = pyqtSignal(str)
	clearCommandLine = pyqtSignal()
	# Initialization point of program.
	def __init__(self, ctrl):
		QObject.__init__(self)
		self.ctrl = ctrl
		self.commandButtonPressed = False
	
	# Create GUI and add all components to it.
	def createGUI(self):
		#Declare Components
		self.app = QApplication(sys.argv)
		self.window = QWidget()

		# Create Grids
		
		#Background Grid:
		self.mainGrid = QGridLayout(self.window)
		
		# Dac specific grid:
		self.dacSpecBG = QWidget(self.window)
		self.dacSpecGrid = QGridLayout(self.dacSpecBG)
		
		# Global Options grid:
		self.globalOptsBG = QWidget(self.window)
		self.globalOptsGrid = QGridLayout(self.globalOptsBG)
		
		# Log Grid:
		self.logBG = QWidget(self.window)
		self.logGrid = QGridLayout(self.logBG)

		# Make startup control components
		
		self.initDACBtn = QPushButton("Initialize DAC", self.window)
		self.loadWaveformBtn = QPushButton("Load csv", self.window)
		self.browseWaveformBtn = QPushButton("Browse...", self.window)
		self.dacSelectCB = QComboBox(self.window)
		self.loadWaveformTB = QLineEdit(self.window)
		
		self.initAllDacBtn = QPushButton("Initialize ALL DACs", self.window)
		self.triggerBtn = QPushButton("Trigger All", self.window)
		self.triggerModeSelRB_Ext = QRadioButton("External Trigger",self.window)
		self.triggerModeSelRB_Man = QRadioButton("Manual Trigger",self.window)
		
		self.outputLogTA = QTextEdit(self.window)
		self.commandTB = QLineEdit(self.window)
		self.inputEnterBtn = QPushButton("Enter", self.window)
		
		# DEBUG COMPONENTS
		self.upBtn = QPushButton("Debug +", self.window)
		self.downBtn = QPushButton("Debug -", self.window)
		self.upBtn.released.connect(self.upLis)
		self.downBtn.released.connect(self.downLis)	
		self.globalOptsGrid.addWidget(self.upBtn, 1, 0)
		self.globalOptsGrid.addWidget(self.downBtn, 1, 1)
		# END DEBUG COMPONENTS
		
		# Configure Components
		# Window
		self.window.setWindowTitle("DAC Control")
		self.window.resize(1000, 800)
		
		# DAC Specific Settings:
		self.dacSelectCB.addItems(["DAC 0", "DAC 1", "DAC 2", "DAC 3", "DAC 4", "DAC 5", "DAC 6", "DAC 7"])
		self.loadWaveformBtn.released.connect(self.loadWFListener)
		self.browseWaveformBtn.released.connect(self.browseWFListener)
		self.initDACBtn.released.connect(self.initDacListener)
		
		# Global Options Grid:
		self.triggerModeSelRB_Man.setChecked(True)
		self.initAllDacBtn.released.connect(self.initAllDacListener)
		self.triggerBtn.released.connect(self.triggerListener)
		self.triggerModeSelRB_Man.toggled.connect(self.manualTrigModeListener)
		self.triggerModeSelRB_Ext.toggled.connect(self.externalTrigModeListener)
		
		# Log Grid
		self.outputLogTA.setReadOnly(True)
		self.outputLogTA.setLineWrapMode(QTextEdit.NoWrap)
		OLfont = self.outputLogTA.font()
		OLfont.setFamily("Courier")
		OLfont.setPointSize(10)
		self.addText.connect(self.outputLogTA.append)
		
		self.clearCommandLine.connect(self.commandTB.clear)
		
		self.inputEnterBtn.released.connect(self.enterListener)
		
		# Add Components
		# Grids
		self.mainGrid.addWidget(self.dacSpecBG, 0, 0)
		self.mainGrid.addWidget(self.globalOptsBG, 1, 0)
		self.mainGrid.addWidget(self.logBG, 2, 0)
		
		# Add Dac Grid Components:
		self.dacSpecGrid.addWidget(self.dacSelectCB, 0, 0)
		self.dacSpecGrid.addWidget(self.loadWaveformTB, 1, 0)
		self.dacSpecGrid.addWidget(self.browseWaveformBtn, 1, 1)
		self.dacSpecGrid.addWidget(self.loadWaveformBtn, 2, 0)
		self.dacSpecGrid.addWidget(self.initDACBtn, 2, 1)
		
		# Add Global Options Grid Components:
		self.globalOptsGrid.addWidget(self.initAllDacBtn, 0, 0)
		self.globalOptsGrid.addWidget(self.triggerBtn, 0, 1)
		self.globalOptsGrid.addWidget(self.triggerModeSelRB_Man, 0, 2)
		self.globalOptsGrid.addWidget(self.triggerModeSelRB_Ext, 0, 3)
		
		# Add Log Grid Components:
		self.logGrid.addWidget(self.outputLogTA, 0, 0)
		self.logGrid.addWidget(self.commandTB, 1, 0)
		self.logGrid.addWidget(self.inputEnterBtn, 1, 1)
		
		self.loadWaveformTB.setText('/home/yelab/GitRepo/SrE/DACs/DAC Frontpanel/dat.csv')
		self.commandTB.setText('1')
		
		self.setComponentEnable(False)
		
		self.window.show()
		
		sys.exit(self.app.exec_())
	
	# Listens for the "+" button.
	def upLis(self):
		self.ctrl.fpga.cnt = self.ctrl.fpga.cnt + 1;
		thread.start_new_thread(FPGACom.startShift, (self.ctrl.fpga,))
		
	# Listens for the "-" button.
	def downLis(self):
		self.ctrl.fpga.cnt = self.ctrl.fpga.cnt - 1;
		thread.start_new_thread(FPGACom.startShift, (self.ctrl.fpga,))
	
	# Listener for loadWaveformBtn
	def loadWFListener(self):
		if self.loadWaveformTB.text() == "":
			self.ctrl.log("Error: File name cannot be empty")
		else:
			thread.start_new_thread(Controller.loadDac, (self.ctrl,self.dacSelectCB.currentIndex(),self.loadWaveformTB.text()))
	
	# Enable/Disable components (except command box and "enter" button)
	def setComponentEnable(self, enable):
		self.initDACBtn.setEnabled(enable)
		self.loadWaveformBtn.setEnabled(enable)
		self.browseWaveformBtn.setEnabled(enable)
		self.dacSelectCB.setEnabled(enable)
		self.loadWaveformTB.setEnabled(enable)
		self.initAllDacBtn.setEnabled(enable)
		self.triggerBtn.setEnabled(enable)
		self.triggerModeSelRB_Ext.setEnabled(enable)
		self.triggerModeSelRB_Man.setEnabled(enable)
		
		self.upBtn.setEnabled(enable)
		self.downBtn.setEnabled(enable)
	
	# Listener for browseWaveformBtn
	def browseWFListener(self):
		dlg = QFileDialog()
		dlg.setFilter("CSV Files (*.csv)")
		self.loadWaveformTB.setText(dlg.getOpenFileName())
	
	# Listener for initDACBtn
	def initDacListener(self):
		thread.start_new_thread(Controller.initDac, (self.ctrl,self.dacSelectCB.currentIndex()))
	
	# Listener for initAllDacBtn
	def initAllDacListener(self):
		thread.start_new_thread(Controller.initAllDac, (self.ctrl,))
	
	# Listener for triggerBtn
	def triggerListener(self):
		thread.start_new_thread(Controller.trigger, (self.ctrl,))
	
	# Listener for external trigger radio button
	def externalTrigModeListener(self, checked):
		if checked:
			self.ctrl.setExtTrig(True)
	
	# Listener for manual trigger radio button
	def manualTrigModeListener(self, checked):
		if checked:
			self.ctrl.setExtTrig(False)
	
	# Command Enter button listener
	def enterListener(self):
		self.commandButtonPressed = True
		thread.start_new_thread(GUI.enterListenerFollowup, (self, ))
	
	# Follow-up for command enter button listener (thread starting point).
	def enterListenerFollowup(self):
		time.sleep(0.01)
		self.commandButtonPressed = False
	
	# Append text to log text area.
	def addTextToLog(self, text):
		self.addText.emit(text)
		
	# Returns current user input.
	def getUserInput(self):
		text = self.commandTB.text()
		self.clearCommandLine.emit()
		return text
		
# This class is the main control of the program. 
class Controller:
	def __init__(self):
		self.gui = GUI(self)
		self.fpga = FPGACom(self)
		self.extMode = False # False = Manual Trigger Mode. True = external trigger mode.
		thread.start_new_thread(FPGACom.connect, (self.fpga, ))
		self.gui.createGUI()
	
	# Enable GUI's components
	def enableGUI(self):
		self.gui.setComponentEnable(True)
	
	# Disable GUI's components
	def disableGUI(self):
		self.gui.setComponentEnable(False)
		
	
	# Load dac 'dac' with csv file 'file'
	def loadDac(self, dac, file):
		self.log("Loading dac {0} with waveform data from file {1}".format(dac, file))
		wf = Waveform(self)
		if wf.error == False:
			wf.loadFromCSV(file)
			self.fpga.loadDACRAM(dac, wf)
			self.log("Done loading dac {0}".format(dac))
		else:
			self.log("Waveform Error encountered while loading dac {0}".format(dac))
			
	# Trigger DACs
	def trigger(self):
		self.fpga.triggerDAC()
	
	# Iterate through all 8 dacs, initializing them.
	def initAllDac(self):
		self.log("Initializing all DACs")
		for i in range(0, 8):
			self.initDac(i)
		#self.fpga.setDacState('idle')
		self.log("Done initializing all DACs")
	
	# Initialize dac 'dac' 
	def initDac(self, dac):
		self.log("Initializing dac {0}".format(dac))
		self.fpga.setupDAC(dac)
		self.log("Done initializing dac {0}".format(dac))
		
	# Set to external trigger mode if set is True
	def setExtTrig(self, set):
		if set:
			self.extMode = True
			self.fpga.setWire1InputBit(0, 1)
			self.log("External trigger mode activated")
		else:
			self.extMode = False
			self.fpga.setWire1InputBit(0, 0)
			self.log("Manual trigger mode activated")
		self.fpga.updateIns()
		
	# Output text to gui log.
	def log(self, text):
		self.gui.addTextToLog(str(text))
	
	# Waits until user releases the "Enter" button for commands and returns the text in the command text box at that moment.
	def getUserInput(self):
		while self.gui.commandButtonPressed == False:
			pass
		self.gui.commandButtonPressed = False
		return self.gui.getUserInput()
# STARTUP #########################################################################

#DAC FrontPanel Starting Point
if __name__ == "__main__":
	# bitlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
	# print bitlist[:-48]
	# print bitlist[-48:-40]
	# print bitlist[-40:-32]
	# print bitlist[-32:-24]
	# print bitlist[-24:-16]
	# print bitlist[-16:-8]
	# print bitlist[-8:]
	ctrl = Controller()
