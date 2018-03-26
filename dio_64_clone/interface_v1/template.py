#GUI 

import sys
import time
#from gmpy2 import *
from PyQt4 import QtGui, QtCore
from blue_lasers import blue_lasers

#Class for blue laser gui
class blue_GUI(QtGui.QWidget):

	def __init__(self):
        	super(blue_GUI, self).__init__()
        	self.initUI()



	def initUI(self):

		#Lock currents for 4, 5, 6
		self.lock_currents = [149.5,149.5,149.5]

		#Call blue class functions for slaves
		self.blues = blue_lasers()

        	grid = QtGui.QGridLayout()
        	self.setLayout(grid)

		#Declaring and propagating buttons/labels/etc        
       		#Row 0 is all labels
		labels_row_0 = ['Laser','Current (mA)', 'Power', 'Lock currents', 'Lock buttons',' ']
		for i in range(0,len(labels_row_0)):
			label = QtGui.QLabel(labels_row_0[i])
			grid.addWidget(label,0,i)

       		#Column for Laser Labels
		labels_lasers = ['MOT', 'TC', 'ZS']
		for i in range(0,len(labels_lasers)):
			label = QtGui.QLabel(labels_lasers[i])
			grid.addWidget(label,1+i,0) 

        	
		#Columns for powers and currentsa, and setcurrents. Store labels in lists for ease of calling.
		self.labels_powers = [QtGui.QLabel("Null"), QtGui.QLabel("Null"), QtGui.QLabel("Null")]
                self.labels_currents = [QtGui.QLabel("Null"), QtGui.QLabel("Null"), QtGui.QLabel("Null")]
		self.line_edits_lock_currents = [QtGui.QLineEdit(str(self.lock_currents[0])),QtGui.QLineEdit(str(self.lock_currents[1])),QtGui.QLineEdit(str(self.lock_currents[2]))]
		for i in range(0,len(self.labels_powers)):
			grid.addWidget(self.labels_currents[i],1+i,1)
			grid.addWidget(self.labels_powers[i],1+i,2)
			grid.addWidget(self.line_edits_lock_currents[i],1+i,3)


		#Row 1
		button_lock_MOT = QtGui.QPushButton("Lock MOT")
                grid.addWidget(button_lock_MOT,1,4)

        	#Row 2 TC 

		#self.label_TC_power = QtGui.QLabel("Null")
                #grid.addWidget(self.label_TC_power,2,2)

		button_lock_TC = QtGui.QPushButton("Lock TC")
                grid.addWidget(button_lock_TC,2,4)
                #buttonUpdateFrequencies.clicked.connect(self.handle_button_lock_TC)


        	#Row 3 ZS
                #self.label_ZS_current = QtGui.QLabel("Null")
                #grid.addWidget(self.label_ZS_current,3,1)

                #self.label_ZS_power = QtGui.QLabel("Null")
                #grid.addWidget(self.label_ZS_power,3,2)

		button_lock_ZS = QtGui.QPushButton("Lock ZS")
                grid.addWidget(button_lock_ZS,3,4)
                #buttonUpdateFrequencies.clicked.connect(self.handle_button_lock_MOT)

		#Row 5 buttons for reading current/power, 
		button_read_blues = QtGui.QPushButton('Read blues')
        	grid.addWidget(button_read_blues,5,0)
        	button_read_blues.clicked.connect(self.handle_button_read_blues)



        	#Moves the window to this screen position.
		self.resize(400,200)
        	self.move(300, 300)


        	self.setWindowTitle('Blue Laser Control GUI')
        	self.show()


	#Read powers and currents
	def handle_button_read_blues(self):
    		#Get powers and currents updated
		self.blues.read_blues()
		
		#Update the powers/currents. 3 Controllers!
		for i in range(0,3):
			self.labels_currents[i].setText(str(self.blues.currents[i]))
			self.labels_powers[i].setText(str(self.blues.powers[i]))
		
		#Add a delay for people rage clicking
		time.sleep(1)


		#[self.label_MOT_current,self.label_TC_current,self.label_ZS_current] = self.blues.currents
		#[self.label_MOT_power,self.label_TC_power,self.label_ZS_power] = self.blues.powers
		






#Defines main to be called to execute the program

def main():

	app = QtGui.QApplication(sys.argv)
	ex = blue_GUI()
	sys.exit(app.exec_())


#Exectures gui
if __name__ == '__main__':
	main()



