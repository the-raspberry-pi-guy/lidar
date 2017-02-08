# Distance Sensing Abstraction Library

import smbus
import sys
import time

class distance(object):
	""" An all-powerful distance sensor controller"""

	VL53L0X_REG_IDENTIFICATION_MODEL_ID             = 0xc0
	VL53L0X_REG_IDENTIFICATION_REVISION_ID          = 0xc2
	VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD       = 0x50
	VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD     = 0x70
	VL53L0X_REG_SYSRANGE_START                      = 0x00

	VL53L0X_REG_RESULT_INTERRUPT_STATUS             = 0x13
	VL53L0X_REG_RESULT_RANGE_STATUS                 = 0x14

	address = 0x29

	bus = smbus.SMBus(1)

	def bswap(self, val):
    		return struct.unpack('<H', struct.pack('>H', val))[0]
	def mread_word_data(self, adr, reg):
    		return bswap(distance.bus.read_word_data(adr, reg))
	def mwrite_word_data(self, adr, reg, data):
    		return distance.bus.write_word_data(adr, reg, distance.bswap(data))
	def makeuint16(self, lsb, msb):
    		return ((msb & 0xFF) << 8)  | (lsb & 0xFF)
	
	@staticmethod	
	def VL53L0X_decode_vcsel_period(vcsel_period_reg):
		# Converts the encoded VCSEL period register value into the real
		# period in PLL clocks
		vcsel_period_pclks = (vcsel_period_reg + 1) << 1;
		return vcsel_period_pclks;

	def get_revision_ID(self):
		ID = distance.bus.read_byte_data(distance.address, distance.VL53L0X_REG_IDENTIFICATION_REVISION_ID)
		return hex(ID)
	
	def get_device_ID(self):
		ID = distance.bus.read_byte_data(distance.address, distance.VL53L0X_REG_IDENTIFICATION_MODEL_ID)
		return hex(ID)

	def get_prerange_config_vcsel_period(self):
		period = distance.bus.read_byte_data(distance.address, distance.VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD)
		output = "Pre range config vcsel period: " + str(hex(period)) + " decode: " + str(distance.VL53L0X_decode_vcsel_period(period))
		return output
	
	def get_finalrange_config_vcsel_period(self):
		period = distance.bus.read_byte_data(distance.address, distance.VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD)
		output = "Final range config vcsel period: " + str(hex(period)) + " decode: " + str(distance.VL53L0X_decode_vcsel_period(period))
		return output
	
	def set_sysrange_start(self):
		sysrange = distance.bus.write_byte_data(distance.address, distance.VL53L0X_REG_SYSRANGE_START, 0x01)	
		return "done sysrange"

	def get_ready_status(self):
		cnt = 0
		while (cnt < 100):
			time.sleep(0.10)
			range_status = distance.bus.read_byte_data(distance.address, distance.VL53L0X_REG_RESULT_RANGE_STATUS)
			if (range_status & 0x01):
				break
			cnt += 1
		if (range_status & 0x01):
			return "ready"
		else:
			return "not ready"

	def get_distance(self):
		data = distance.bus.read_i2c_block_data(distance.address, 0x14, 12)
		output = int(distance.makeuint16(self, data[11], data[10]))
		return output

d = distance()
print d.get_revision_ID()
print d.get_device_ID()
print d.get_prerange_config_vcsel_period()
print d.get_finalrange_config_vcsel_period()
print d.get_ready_status()
while True:
#	time.sleep(0.2)
	d.set_sysrange_start()
	val = d.get_distance()
	if val == 20:
		print "Failed"
	else:
		print val
