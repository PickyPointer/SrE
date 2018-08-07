import time
from shutil import copyfile
from os import listdir, rename
from os.path import isfile, join
onlyfiles = [f for f in listdir("C:/Users/jas24/OneDrive/Ye Group/Projects/DACs/DAC Frontpanel/bitfiles_old") if isfile(join("C:/Users/jas24/OneDrive/Ye Group/Projects/DACs/DAC Frontpanel/bitfiles_old", f))]

i = 1
while True:
	try:
		onlyfiles.index('dac_fpga_bitstream{0}.bit'.format(i))
		i += 1
	except ValueError:
		if isfile("C:/Users/jas24/OneDrive/Ye Group/Projects/DACs/DAC Frontpanel/dac_fpga_bitstream.bit"):
			rename("C:/Users/jas24/OneDrive/Ye Group/Projects/DACs/DAC Frontpanel/dac_fpga_bitstream.bit", "C:/Users/jas24/OneDrive/Ye Group/Projects/DACs/DAC Frontpanel/bitfiles_old/dac_fpga_bitstream{0}.bit".format(i))
		break		

try:
	copyfile("C:/Users/jas24/OneDrive/Ye Group/Projects/DACs/FPGA VHDL Programming/DAC/DAC.runs/impl_1/control.bit", "C:/Users/jas24/OneDrive/Ye Group/Projects/DACs/DAC Frontpanel/dac_fpga_bitstream.bit")
except:
	raw_input("error\nPress enter to continue...")