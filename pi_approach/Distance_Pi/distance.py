# Lidar Project Distance Subsystem

import serial
import socket
import time
import sys
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
import serverxclient as cli

arduino_dist = serial.Serial('/dev/ttyUSB0',9600)

def get_distance():
	distance = arduino_dist.readline()
	return distance

def main():
	client = cli.Client()
	connected = False
	while not connected:
		try:
			client.socket_connection()
			connected = True
		except:
			print "Failure"
			time.sleep(2)
	
	hand_shake = "DISTANCE!"
	client.send_data(hand_shake)
	client.close_connection()

main()
