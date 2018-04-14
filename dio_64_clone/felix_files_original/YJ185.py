import usb
import time
import math
import serial

class DIO64_POINT:
    def __init__(self, time, P1, P2, P3, P4, P5, P6, P7, P8):
        self.time = time
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4
        self.P5 = P5
        self.P6 = P6
        self.P7 = P7
        self.P8 = P8

class DIO64(object):
    NUMPOINTS         = 2048
    MSGLENGTH         = 7
    TIMEOFFS          = 0x0800
    BANKAOFFS         = 0x1000
    BANKBOFFS         = 0x1800
    WBWRITE           = 161
    WRITESPERDATAPT   = 3
    BUFFERSIZESER     = 100
    
    def __init__(self, port=1, showserial = False, showdebug = False):
        self.serial = serial.Serial(str(port), 115200) #open serial port
        self.showdebug  = showdebug
        self.showserial = showserial
        if(showdebug):
            print self.serial.name
        self.mem = [DIO64_POINT(0,0,0,0,0,0,0,0,0) for i in range(self.NUMPOINTS)]

    def setPoint(self, number, time, P1, P2, P3, P4, P5, P6, P7, P8):
        self.mem[number].time   = time
        self.mem[number].P1     = P1
        self.mem[number].P2     = P2
        self.mem[number].P3     = P3
        self.mem[number].P4     = P4
        self.mem[number].P5     = P5
        self.mem[number].P6     = P6
        self.mem[number].P7     = P7
        self.mem[number].P8     = P8

    def setPointObj(self, number, DIO64_POINT):
        self.mem[number] = DIO64_POINT

    def getPoint(self, number):
        return [self.mem[number].time,
                self.mem[number].P1,
                self.mem[number].P2,
                self.mem[number].P3,
                self.mem[number].P4,
                self.mem[number].P5,
                self.mem[number].P6,
                self.mem[number].P7,
                self.mem[number].P8]

    def getPointObj(self, number):
        return self.mem[number]

    def trigger(self):
        data = []
        data.append(self.WBWRITE)
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(1)

        if(self.showserial):
            print data
        self.serial.write(data)

    def write(self):
        count = 0
        for timestamp in self.mem:
            data = []
            data.append(self.WBWRITE)
            data.append(((self.TIMEOFFS + count) & 0xff00) >> 8)
            data.append(((self.TIMEOFFS + count) & 0x00ff) >> 0)
            data.append((timestamp.time & 0xff000000) >> 24)
            data.append((timestamp.time & 0x00ff0000) >> 16)
            data.append((timestamp.time & 0x0000ff00) >>  8)
            data.append((timestamp.time & 0x000000ff) >>  0)

            if(self.showserial):
                print data
            self.serial.write(data)
            
            data = []
            data.append(self.WBWRITE)
            data.append(((self.BANKAOFFS + count) & 0xff00) >> 8)
            data.append(((self.BANKAOFFS + count) & 0x00ff) >> 0)
            data.append(timestamp.P1)
            data.append(timestamp.P2)
            data.append(timestamp.P3)
            data.append(timestamp.P4)

            if(self.showserial):
                print data
            self.serial.write(data)
            
            data = []
            data.append(self.WBWRITE)
            data.append(((self.BANKBOFFS + count) & 0xff00) >> 8)
            data.append(((self.BANKBOFFS + count) & 0x00ff) >> 0)
            data.append(timestamp.P5)
            data.append(timestamp.P6)
            data.append(timestamp.P7)
            data.append(timestamp.P8)

            if(self.showserial):
                print data
            self.serial.write(data)
            
            count = count + 1
            
            if (    timestamp.time == 0 and
                    timestamp.P1 == 0 and
                    timestamp.P2 == 0 and
                    timestamp.P3 == 0 and
                    timestamp.P4 == 0 and
                    timestamp.P5 == 0 and
                    timestamp.P6 == 0 and
                    timestamp.P7 == 0 and
                    timestamp.P8 == 0):
                break
