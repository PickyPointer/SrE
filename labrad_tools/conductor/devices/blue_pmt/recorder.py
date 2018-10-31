import json
from twisted.internet.defer import inlineCallbacks
import time
import os
import numpy as np

from conductor_device.conductor_parameter import ConductorParameter

class Recorder(ConductorParameter):
    priority = 9
    data_dir = '/home/srgang/J/data/{}/scans/{}#{}/'
    data_filename = '{}.blue_pmt'
    pmt_sequences = [
        'lattice_sb_linescan',
        'sf_red_some_bs',
        'lattice_pol_p_linescan',
        'lattice_pol_m_linescan',
        'lattice_pol_m_noClock',
        'sf_red_some_test',
        'lattice_mF_scan',
        'co_pulse_plus',
        'co_pulse_minus',
	'lattice_pol_mF_scan',
	'ramsey_pol_p',
	'ramsey_pol_m',
        ]
    save_raw_data = True

    @inlineCallbacks
    def initialize(self):
        yield self.connect()
        yield self.cxn.pmt.select_device('blue_pmt')
    
    @inlineCallbacks
    def update(self):
        date_str = time.strftime('%Y%m%d')
        exp_name = self.conductor.experiment_name
        exp_num = self.conductor.experiment_number
        exp_pt = self.conductor.point_number
        run_dir = self.data_dir.format(date_str, exp_name, exp_num)
        
        pt_filename = self.data_filename.format(exp_pt)
        pt_path = run_dir + pt_filename

        
        sequence = self.conductor.parameters['sequencer']['sequence'].value
        if np.intersect1d(sequence, self.pmt_sequences):
            yield self.cxn.pmt.record(pt_path, self.save_raw_data)
        else:
            print self.pmt_sequences
            print 'pmt sequence not found'
