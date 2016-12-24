# Distance Sensing Abstraction Library

import smbus
import sys
import time

class distance_sensor(object):
	""" An all-powerful distance sensor controller"""

	VL53L0X_REG_IDENTIFICATION_MODEL_ID             = 0x00c0
	VL53L0X_REG_IDENTIFICATION_REVISION_ID          = 0x00c2
	VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD       = 0x0050
	VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD     = 0x0070
	VL53L0X_REG_SYSRANGE_START                      = 0x000

	VL53L0X_REG_RESULT_INTERRUPT_STATUS             = 0x0013
	VL53L0X_REG_RESULT_RANGE_STATUS                 = 0x0014

	address = 0x29

	bus = smbus.SMBus(1)

	def bswap(self, val):
    		return struct.unpack('<H', struct.pack('>H', val))[0]
	def mread_word_data(self, adr, reg):
    		return bswap(bus.read_word_data(adr, reg))
	def mwrite_word_data(self, adr, reg, data):
    		return bus.write_word_data(adr, reg, bswap(data))
	def makeuint16(self, lsb, msb):
    		return ((msb & 0xFF) << 8)  | (lsb & 0xFF)
	def VL53L0X_decode_vcsel_period(self,vcsel_period_reg):
		# Converts the encoded VCSEL period register value into the real
		# period in PLL clocks
		vcsel_period_pclks = (vcsel_period_reg + 1) << 1;
		return vcsel_period_pclks;

	def get_revision_ID(self):
		ID = bus.read_byte_data(address, distance_sensor.VL53L0X_REG_IDENTIFICATION_REVISION_ID)
		return hex(ID)
	
	def get_device_ID(self):
		ID = bus.read_byte_data(address, distance_sensor.VL53L0X_REG_IDENTIFICATION_MODEL_ID)
		return hex(ID)

	def get_prerange_config_vcsel_period(self):
		period = bus.read_byte_data(address, distance_sensor.VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD)
		output = "Final range config vcsel period: " + hex(period) + " decode: " + str(distance_sensor.VL53L0X_decode_vcsel_period(period)
		return output
