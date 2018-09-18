import devices.yesr_analog_board.yesr_analog_board
reload(devices.yesr_analog_board.yesr_analog_board)
from devices.yesr_analog_board.yesr_analog_board import YeSrAnalogBoard
from devices.yesr_analog_board.lib.analog_channel import AnalogChannel

class BoardE(YeSrAnalogBoard):
    okfpga_server_name = 'yeelmo_okfpga'
    okfpga_device_id = 'Ross_DAC_1'

    bitfile = 'analog_sequencer-v2b.bit'
#    bitfile = 'analog_sequencer.bit'

    autostart = True

    channels = [
        AnalogChannel(loc=0, name='MOT Ramp', mode='auto', manual_output=0.0),
        AnalogChannel(loc=1, name='H2 Bias', mode='auto', manual_output=0.0),
        AnalogChannel(loc=2, name='Lattice Ramp', mode='auto', manual_output=0.0),
        AnalogChannel(loc=3, name='DC Stark A', mode='auto', manual_output=0.0),
        AnalogChannel(loc=4, name='DC Stark B', mode='auto', manual_output=0.0),
        AnalogChannel(loc=5, name='DC Stark C', mode='auto', manual_output=0.0),
        AnalogChannel(loc=6, name='DC Stark D', mode='auto', manual_output=0.0),
        AnalogChannel(loc=7, name='Zeeman Intensity', mode='auto', manual_output=0.0),
        ]


__device__ = BoardE
