# Lidar Project Distance Subsystem

import serial
import socket
import time

arduino_dist = serial.Serial('/dev/ttyUSB0',9600)

def get_distance():
	distance = arduino_dist.readline()
	return distance

class Client(object):
	"""A class that uses sockets to connect to a server"""
	HOST = "userinterface.local"
	PORT = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def socket_connection(self):
		Client.s.connect((Client.HOST, Client.PORT))
	
	def receive_data(self):
		data = Client.s.recv(4096)
		return data
	
	def send_data(self, data):
		Client.s.send(data)

client = Client()
client.socket_connection()
while True:
	client.send_data("Hello! Yo!")
	time.sleep(1)
