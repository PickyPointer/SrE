#GUI 

import sys
import time
#from gmpy2 import *
from PyQt4 import QtGui, QtCore


#Class for blue laser gui
class dio_gui(QtGui.QWidget):

	def __init__(self):
        	super(dio_gui, self).__init__()
        	self.initUI()



	def initUI(self):



        	grid = QtGui.QGridLayout()

		#Set no spacing between grid
		grid.setHorizontalSpacing(0)
		grid.setVerticalSpacing(0)
        	self.setLayout(grid)

		#Spec num rows and columns
		self.num_rows = 32 #64 TTL's, 1 for times
		self.num_columns = 20

		#Declaring and propagating buttons/labels/etc        
       		#Row 0 is all labels
		labels_row_0 = ['Laser','Current (mA)', 'Power', 'Lock currents', 'Lock buttons',' ']
		for i in range(0,self.num_columns):
			label = QtGui.QLabel(str(i))
			grid.addWidget(label,0,i+1)

		#Propogate buttons
		for i in range(0,self.num_rows):
			for j in range(0,self.num_columns):
       				button = QtGui.QPushButton("")
				button.setFixedSize(40,40)				
				grid.addWidget(button,i+1,j+1)

        	


		


        	#Moves the window to this screen position.
		self.resize(400,200)
        	#self.move(300, 300)


        	self.setWindowTitle('SrE Timing Interface')
        	self.show()



		






#Defines main to be called to execute the program

def main():

	app = QtGui.QApplication(sys.argv)
	ex = dio_gui()
	sys.exit(app.exec_())


#Exectures gui
if __name__ == '__main__':
	main()



