# -*- coding: utf-8 -*-
#!/usr/bin/python

import RPi.GPIO as GPIO
import os
import smbus
import time
import datetime
import ambient

#Input your ambients ID or writeKey
ambi = ambient.Ambient(ID,'writeKey')

# ADXL345 Class
class ADXL345():
	DevAdr = 0x53
	myBus = ""
	if GPIO.RPI_INFO['P1_REVISION'] == 1:
		myBus = 0
	else:
		myBus = 1
	b = smbus.SMBus(myBus)

	def setUp(self):
		self.b.write_byte_data(self.DevAdr, 0x2C, 0x0B) # BandwidthRate
		self.b.write_byte_data(self.DevAdr, 0x31, 0x00) # DATA_FORMAT 10bit 2g
		self.b.write_byte_data(self.DevAdr, 0x38, 0x00) # FIFO_CTL OFF
		self.b.write_byte_data(self.DevAdr, 0x2D, 0x08) # POWER_CTL Enable

	def getValueX(self):
		return self.getValue(0x32)

	def getValueY(self):
		return self.getValue(0x34)

	def getValueZ(self):
		return self.getValue(0x36)

	def getValue(self, adr):
		tmp = self.b.read_byte_data(self.DevAdr, adr+1)
		sign = tmp & 0x80
		tmp = tmp & 0x7F
		tmp = tmp<<8
		tmp = tmp | self.b.read_byte_data(self.DevAdr, adr)

		if sign > 0:
			tmp = tmp - 32768
		return tmp

# MAIN
myADXL345 = ADXL345()
myADXL345.setUp()

msg = []

# LOOP
ii = 0
roop_cy = 499
for a in range(roop_cy):

	tmsg = {'created': str(datetime.datetime.now()), 'd1': myADXL345.getValueX(), 'd2': myADXL345.getValueY(), 'd3': myADXL345.getValueZ()}
	msg.append(tmsg)
	#time.sleep(0.05)

sent = ambi.send(msg)
sent.close()

