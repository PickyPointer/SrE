import json
import h5py
import os
from PyQt4 import QtGui, QtCore
from twisted.internet.defer import inlineCallbacks, returnValue
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sys

from client_tools.connection import connection

class MplCanvas(FigureCanvas):
    def __init__(self):
#        self.fig = Figure()
#        self.axes = self.fig.add_subplot(111)
        fig, ax = plt.subplots(1)
        self.fig = fig
        self.ax = ax

        self.fig.set_tight_layout(True)

        FigureCanvas.__init__(self, self.fig)
        self.setFixedSize(800, 400)

#    def plot(self, y, label=None):
#        self.ax.set_xlabel('time [s]')
#        self.ax.set_ylabel('voltage [V]')
#        self.ax.plot(y, label=label)
#        self.ax.legend()

class PMTViewer(QtGui.QDialog):
    if sys.platform == "win32":
        data_dir = 'J:\\data\\'
    else:
        data_dir = '/home/srgang/J/data/'

    def __init__(self, pmt_name, reactor, cxn=None):
        super(PMTViewer, self).__init__(None)
        self.pmt_name = pmt_name
        self.reactor = reactor
        self.cxn = cxn

        self.update_id = np.random.randint(0, 2**31 - 1)
#        self.update_id = 6100034
        self.loading = False
        self.connect()
   
    @inlineCallbacks
    def connect(self):
        if self.cxn is None:
            self.cxn = connection()
            cname = 'pmt - {} - client'.format(self.pmt_name)
            yield self.cxn.connect(name=cname)
#        self.context = yield self.cxn.context()

        self.populate()
        yield self.connect_signals()
        #self.replot()

    def populate(self):
        self.setWindowTitle(self.pmt_name)
        self.canvas = MplCanvas()
        self.nav = NavigationToolbar(self.canvas, self)
        self.lcdGND = QtGui.QLCDNumber(self)
        self.lcdGND.display('0.001')
        self.lcdEXC = QtGui.QLCDNumber(self)
        self.lcdEXC.display('0.001')
        self.lcdBAC = QtGui.QLCDNumber(self)
        self.lcdBAC.display('0.000')
        self.lcdFRAC = QtGui.QLCDNumber(self)
        self.lcdFRAC.display('0.000')
        self.lcdTOTAL = QtGui.QLCDNumber(self)
        self.lcdTOTAL.display('0.000')
        self.labelGND = QtGui.QLabel('GROUND')
        self.labelGND.setAlignment(QtCore.Qt.AlignCenter)
        self.labelGND.setFont(QtGui.QFont("Arial", 48, QtGui.QFont.Bold))
        self.labelEXC = QtGui.QLabel('EXCITED')
        self.labelEXC.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEXC.setFont(QtGui.QFont("Arial", 48, QtGui.QFont.Bold))
        self.labelBAC = QtGui.QLabel('BACKGROUND')
        self.labelBAC.setAlignment(QtCore.Qt.AlignCenter)
        self.labelBAC.setFont(QtGui.QFont("Arial", 48, QtGui.QFont.Bold))
        self.labelFRAC = QtGui.QLabel('EXC. FRACTION')
        self.labelFRAC.setAlignment(QtCore.Qt.AlignCenter)
        self.labelFRAC.setFont(QtGui.QFont("Arial", 48, QtGui.QFont.Bold))
        self.labelTOTAL = QtGui.QLabel('TOTAL')
        self.labelTOTAL.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTOTAL.setFont(QtGui.QFont("Arial", 48, QtGui.QFont.Bold))

         
        self.layout = QtGui.QGridLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.layout.addWidget(self.nav)
        self.layout.addWidget(self.canvas)
        
        self.hboxFRAC = QtGui.QHBoxLayout()
        self.hboxFRAC.addWidget(self.labelFRAC)
        self.hboxFRAC.addWidget(self.lcdFRAC)        
        self.hboxGND = QtGui.QHBoxLayout()
        self.hboxGND.addWidget(self.labelGND)
        self.hboxGND.addWidget(self.lcdGND)
        self.hboxEXC = QtGui.QHBoxLayout()
        self.hboxEXC.addWidget(self.labelEXC)
        self.hboxEXC.addWidget(self.lcdEXC)
        self.hboxBAC = QtGui.QHBoxLayout()
        self.hboxBAC.addWidget(self.labelBAC)
        self.hboxBAC.addWidget(self.lcdBAC)
        self.hboxTOTAL = QtGui.QHBoxLayout()
        self.hboxTOTAL.addWidget(self.labelTOTAL)
        self.hboxTOTAL.addWidget(self.lcdTOTAL)
        

        self.layout.addItem(self.hboxFRAC)
        self.layout.addItem(self.hboxGND)
        self.layout.addItem(self.hboxEXC)
        self.layout.addItem(self.hboxBAC)
        self.layout.addItem(self.hboxTOTAL)


        self.setLayout(self.layout)
       
        width = self.canvas.width() + 500
        height = self.nav.height() + self.canvas.height() + 8*self.lcdGND.height() + 200
        self.setFixedSize(width, height)
        self.setWindowTitle('PMT_trace_viewer')
#        yield self.replot()

    @inlineCallbacks
    def connect_signals(self):
        # pyqt signals

        # labrad signals
        pmt_server = yield self.cxn.get_server('pmt')
        yield pmt_server.select_device(self.pmt_name)
        yield pmt_server.signal__update(self.update_id)
        yield pmt_server.addListener(listener=self.receive_update, source=None, ID=self.update_id)

    @inlineCallbacks
    def receive_update(self, c, signal):
        if signal == self.pmt_name:
            pmt_server = yield self.cxn.get_server('pmt')
            data_json = yield pmt_server.retrive(-1)
            data = json.loads(data_json)
            record_name = data['record_name'].split('/')[5:]
            raw_data_path = self.data_dir + os.path.join(*record_name) + '.hdf5'
            self.replot(raw_data_path)
            self.update_numbers(raw_data_path)

    def replot(self, data_path):
        with h5py.File(data_path) as h5f:
            gnd = h5f['gnd'][500:]
            exc = h5f['exc'][500:]
            bac = h5f['bac'][500:]
            self.canvas.ax.clear()
            self.canvas.ax.plot(gnd, label='GND')
            self.canvas.ax.plot(exc, label='EXC')
            self.canvas.ax.plot(bac, label='BAC')
            self.canvas.ax.text(100, 100, 'FRAC')
            self.canvas.ax.legend()
        self.canvas.draw()

    def update_numbers(self, data_path):
        with h5py.File(data_path) as h5f:
            gnd = np.mean(h5f['gnd'][3000:23000])
            exc = np.mean(h5f['exc'][3000:23000])
            bac = np.mean(h5f['bac'][3000:23000])
            tot = (gnd+exc-2*bac)
            if tot==0:
                frac = 0
            else:
                frac = (exc-bac)/tot
            self.lcdGND.display(str(np.round(gnd,3)))
            self.lcdEXC.display(str(np.round(exc,3)))
            self.lcdBAC.display(str(np.round(bac,3)))
            self.lcdFRAC.display(str(np.round(frac,3)))
            self.lcdTOTAL.display(str(np.round(tot,3)))

    
    def closeEvent(self, x):
        self.reactor.stop()

if __name__ == '__main__':
    a = QtGui.QApplication([])
    a.setWindowIcon(QtGui.QIcon('icon.png'))
    import client_tools.qt4reactor as qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    widget = PMTViewer('blue_pmt', reactor)
    widget.show()
    reactor.run()
