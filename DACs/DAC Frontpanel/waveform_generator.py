import time
import sys
import thread
import os
import numpy as np
import math

from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT, QObject, pyqtSignal
from multiprocessing import Lock
def opFromStr(str):
	return {
	'^'
	'*'
	'+'
	'-'
	'/'
	'sin'
	'cos'
	'tan'
	'asin'
	'acos'
	'atan'
	}.get(str,'+')
def constFromStr(str):
	return {
	'e': math.exp(1),
	'pi':
	
	}.get(str,'e')
class f:
	