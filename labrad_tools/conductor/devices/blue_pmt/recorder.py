import json
from twisted.internet.defer import inlineCallbacks
import time
import os
import numpy as np

from conductor_device.conductor_parameter import ConductorParameter

class Recorder(ConductorParameter):
    priority = 2
    data_dir = '/media/z/SrE/Data/{}/{}#{}/'
    #data_filename = 'test_pmt-{}.json'
    data_filename = '{}.blue_pmt'
    pmt_sequences = ['lattice_sb_linescan']
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
            yield self.cxn.pmt.record(pt_path)
        else:
            print self.pmt_sequences
            print sequence
            print 'pmt sequence not found'
