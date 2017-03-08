# distance.py
# Code to control the distance-finding subsytem
# Networked to provide wireless setting and reporting
# Author: Matthew Timmons-Brown

# Import necessary libraries for control of different aspects
import serial
import socket
import time
import sys
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
# Import library that I have created to make communication and control easier
import serverxclient as cli

powerdown = ["sudo", "shutdown", "now"]

# Create class instances for the serial distance connection and network
arduino_dist = serial.Serial('/dev/ttyUSB0',9600)
client = cli.Client()

class distance_controller(object):
	"""A distance-finding controller"""

	# Get distance method
	# Reads and returns the distance reported from Arduino over serial
	def get_distance(self):
		distance = arduino_dist.readline()
		return distance

	# Handshake method
	# Attempts connection with the wireless user interface and
	# verifies the subsytem
	def setup_handshake(self):
		connected = False
		# Repeat until connected
		while not connected:
			try:
				client.socket_connection()
				connected = True
			except:
				print "Failure"
				time.sleep(2)
		received_communication = client.receive_data()
		# Actual handshake process, awaiting verification message
		if received_communication == "VERIFY?":
			hand_shake = "DISTANCE!"
			client.send_data(hand_shake)
		else:
			print "Unidentified communication"

	# Active listen method
	# Waits for communication from the wireless user interface
	# and then acts upon communication
	def active_listen(self):
		received_communication = client.receive_data()
		# Verify distance data and send
		if received_communication == "FIRE":
			result = self.get_distance()
			try:
				test_int = int(result)
				print result
				client.send_data(result)
			# If data is unexpected/corrupted
			except:
				print "Unexpected character"
				client.send_data("0")
		# Power down
		if received_communication == "POWER-OFF":
			subprocess.call(powerdown)

	# Main method
	# Run handshake and then forever runs active listening method
	def main(self):
		self.setup_handshake()
		while True:
			self.active_listen()

# Create class instance and run program
if __name__ == "__main__":
	distance = distance_controller()
	distance.main()
