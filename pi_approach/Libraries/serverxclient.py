# Server and Client Abstraction Library
# Code to control common networking functions of the LIDAR project
# Uses Python sockets to create connections between
# Raspberry Pis on local network
# Code for both server and client
# Author: Matthew Timmons-Brown

# Import necessary library for socket control
import socket

# Set constants of communication
HOST = "userinterface.local"
PORT = 12345

class Server(object):
	"""A server-serving class"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Setup server method
	# Tries to bind the server and reports on any errors of
	# server setup process
	def setup_server(self):
		try:
			Server.s.bind((HOST,PORT))
			print "Bind success"
		except socket.error:
			return "Bind failure"

	# Socket reception method
	# Listens for incoming connections and creates socket
	# Returns connection and address
	def socket_reception(self):
		Server.s.listen(5)
		(connection, address) = Server.s.accept()
		print str(connection)+ " : " + str(address)
		return (connection, address)

	# Receive data method
	# Receives data from the connection argument and returns data buffer
	def receive_data(self, connection):
		data = connection.recv(4096)
		return data

	# Send data method
	# Sends the data argument to the connection argument
	def send_data(self, connection, data):
		connection.send(data)

	# Close connection method
	# Closes connection argument
	def close_connection(self, connection):
		connection.close()

class Client(object):
	"""A socket-enabled client class that connects to a server"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Socket connection method
	# Attempts to connect to the host and port number
	def socket_connection(self):
		Client.s.connect((HOST,PORT))

	# Receive data method
	# Receives data from connection and returns it
	def receive_data(self):
		data = Client.s.recv(4096)
		return data

	# Send data method
	# Sends the data argument to the server
	def send_data(self, data):
		Client.s.send(data)

	# Close connection method
	# Closes the connection between the client and the server
	def close_connection(self):
		Client.s.close()
