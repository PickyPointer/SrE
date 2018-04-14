from YJ185 import DIO64
from YJ185 import DIO64_POINT

NUMPOINTS = 2048 #maximum is 2048

#create a DIO64 object on COM5
DIO = DIO64(port = '/dev/ttyUSB1',showserial = True)
#set a point using numbers
DIO.setPoint(0,100,1,2,3,4,5,6,7,8)
print DIO.getPoint(0)

#set a point using DIO64_POINT object
point = DIO64_POINT(200,9,10,11,12,13,14,15,16)
DIO.setPointObj(1,point)
print DIO.getPointObj(1).time
print DIO.getPointObj(1).P4

#let's write a test pattern
#box will put all outputs high for 1 sec
#wait 2 sec
#put all outputs high for another sec
#notice how all outputs are turned off in point 3 - they will stay high otherwise
#and that the sequence needs a terminator (point 4)
DIO.setPoint(0,0,255,255,255,255,255,255,255,255)
DIO.setPoint(1,200000000,0,0,0,0,0,0,0,0)
DIO.setPoint(2,400000000,255,255,255,255,255,255,255,255)
#DIO.setPoint(3,400000000,0,0,0,0,0,0,0,0)
DIO.setPoint(3,0,0,0,0,0,0,0,0,0) #sequence termination - DIO64 will stop here and be ready for next trigger

DIO.write()

DIO.trigger()
