# Lidar Project Distance Subsystem

import serial
import socket
import time
import sys
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
import serverxclient as cli

powerdown = ["sudo", "shutdown", "now"]

arduino_dist = serial.Serial('/dev/ttyUSB0',9600)
client = cli.Client()

class distance_controller(object):
	"""An all-powerful distance-finding controller"""

	def get_distance(self):
		distance = arduino_dist.readline()
		return distance

	def setup_handshake(self):
		connected = False
		while not connected:
			try:
				client.socket_connection()
				connected = True
			except:
				print "Failure"
				time.sleep(2)
		received_communication = client.receive_data()
		if received_communication == "VERIFY?":
			hand_shake = "DISTANCE!"
			client.send_data(hand_shake)
		else:
			print "Unidentified communication"

	def active_listen(self):
		received_communication = client.receive_data()
		if received_communication == "FIRE":
			result = self.get_distance()
			try:
				test_int = int(result)
				print result
				client.send_data(result)
			except:
				print "Unexpected character"
				client.send_data("0")
		if received_communication == "POWER-OFF":
			subprocess.call(powerdown)

	def main(self):
		self.setup_handshake()
		while True:
			self.active_listen()

distance = distance_controller()
distance.main()
