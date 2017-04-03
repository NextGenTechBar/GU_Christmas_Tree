#!/usr/bin/python

import smbus
import sys

#Set Up i2c Bus
bus = smbus.SMBus(1)

ARD1_ADDRESS =  0x04

#Commands
NULL      = 0
TURN_OFF  = 1 #No Arguments
SET_COLOR = 2 #Followed by a tripplet

cmd = int(sys.argv[1])

print "Trying to send command: {} to {}".format(cmd,ARD1_ADDRESS)

if cmd == TURN_OFF :
	bus.write_i2c_block_data(ARD1_ADDRESS,cmd,[0])
elif cmd == SET_COLOR :
	if len(sys.argv) >= 4 :
		test_vals = [int(sys.argv[2]), int(sys.argv[3]) , int(sys.argv[4])]
		bus.write_i2c_block_data(ARD1_ADDRESS,cmd,test_vals)
	else :
		print "Not Enough Values with SET_COLOR command. Need a color tripplet"
else :
	print "Unknow Command {}".format(cmd)

#bus.write_i2c_block_data(DEVICE_ADDRESS,DEVICE_REG_LEDOUT0, ledout_values)
#test_vals = [int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])]
#bus.write_i2c_block_data(ARD1_ADDRESS,int(sys.argv[1]),test_vals)
