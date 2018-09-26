import json
#import h5py
import os
import numpy as np
from PyQt4 import QtGui, QtCore
from twisted.internet.defer import inlineCallbacks, returnValue

import client_tools.qt4reactor as qt4reactor

import sys
#import labrad

#Use client tool for connecting to Sr 2 labrad server
from client_tools.connection2 import connection2 as connection


class WavemeterViewer(QtGui.QDialog):
    def __init__(self, wm_channel, reactor, cxn=None):
        super(WavemeterViewer, self).__init__(None)
        self.wm_channel = wm_channel
        self.reactor = reactor
        self.cxn = cxn
        #Change this to specify wavemeter frequency corresponding to 
        #the magic wavelength 
        self.target_freq = 368.55445
        #Indicate error if freq differs from target by this amount (THz):
        self.target_threshold = 0.0002

        self.update_id = np.random.randint(0, 2**31 - 1)
#        self.update_id = 6100034
        self.loading = False
        self.connect()
   
    @inlineCallbacks
    def connect(self):
        if self.cxn is None:
            self.cxn = connection()
            cname = 'wavemeter - Ch {} - client'.format(str(self.wm_channel))
            yield self.cxn.connect(name=cname)
        self.context = yield self.cxn.context()
        self.populate()
        yield self.connect_signals()
        yield self.query_frequency()
        
    def populate(self):
        self.setWindowTitle('Wavemeter Ch ' + str(self.wm_channel))
        self.lcd813 = QtGui.QLCDNumber(self)
        self.lcd813.setDigitCount(12)
        self.lcd813.display(324.2498765)

        self.label813 = QtGui.QLabel('LATTICE FREQ')
        #self.label813.setStyleSheet('color: black')
        self.label813.setAlignment(QtCore.Qt.AlignCenter)
        self.label813.setFont(QtGui.QFont("Arial", 48, QtGui.QFont.Bold))    
        
        self.layout = QtGui.QGridLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.hbox813 = QtGui.QHBoxLayout()
        self.hbox813.addWidget(self.label813)
        self.hbox813.addWidget(self.lcd813) 

        self.layout.addItem(self.hbox813)
        #self.layout.addItem(self.btn)
        self.setLayout(self.layout)
        
        width = 2*self.label813.width() 
        height = 0.25*self.label813.height() 
        self.setFixedSize(width, height)
        
        self.show()
        
    @inlineCallbacks
    def connect_signals(self):
        # pyqt signals

        # labrad signals
        wm_server = yield self.cxn.get_server('yesr8_hfwm')
        yield wm_server.signal__update(self.update_id)
        yield wm_server.addListener(listener=self.receive_update, source=None, ID=self.update_id)
        
#    @inlineCallbacks
    def receive_update(self, c, signal_json):
        #yield None
        signal = json.loads(signal_json)
        freq = signal.get('3', {}).get('frequency')
        #wm_server = yield self.cxn.get_server('yesr8_hfwm')
        #frequency = yield wm_server.get_frequency(self.wm_channel)
        #print freq
        if freq !=None:
            #print 'Setting frequency: %f THz'%(freq)
            self.update_frequency(freq)
    
    def update_frequency(self, freq):
        self.lcd813.display(freq)
        #Indicate if the lattice has come unlocked by comparing
        #wavemeter freq with target frequency
        if np.abs(freq-self.target_freq)>=self.target_threshold:
            self.label813.setStyleSheet('color: red')
        else:
            self.label813.setStyleSheet('color: black')
            
    @inlineCallbacks   
    def query_frequency(self):
        wm_server = yield self.cxn.get_server('yesr8_hfwm')
        frequency = yield wm_server.get_frequency(self.wm_channel)
        reactor.callLater(1.0, self.query_frequency)

    def closeEvent(self, x):
        self.reactor.stop()
        
if __name__ == '__main__':
    a = QtGui.QApplication([])
    #a.setWindowIcon(QtGui.QIcon('icon.png'))

    qt4reactor.install()
    
    from twisted.internet import reactor
    widget = WavemeterViewer(3, reactor)
    widget.show()
    reactor.run()
