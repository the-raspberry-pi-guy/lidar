# Server and Client Abstraction Library

import socket

HOST = "userinterface.local"
PORT = 12345

class Server(object):
	"""A server-serving class"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def setup_server(self):
		try:
			Server.s.bind((HOST,PORT))
			print "Bind success"
		except socket.error:
			return "Bind failure"

	def socket_reception(self):
		Server.s.listen(5)
		(connection, address) = Server.s.accept()
		print str(connection)+ " : " + str(address)
		return (connection, address)

	def receive_data(self, connection):
		data = connection.recv(4096)
		return data

	def send_data(self, connection, data):
		connection.send(data)
	
	def close_connection(self, connection):
		connection.close()

class Client(object):
	"""A socket-enabled client class that connects to a server"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def socket_connection(self):
		Client.s.connect((HOST,PORT))

	def receive_data(self):
		data = Client.s.recv(4096)
		return data

	def send_data(self, data):
		Client.s.send(data)
