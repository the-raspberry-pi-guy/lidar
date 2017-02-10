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

client = cli.Client()
client.socket_connection()
while True:
	client.send_data("Hello! Yo!")
	time.sleep(1)
