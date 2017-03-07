# lidar.py
# Code to control the touchscreen user interface subsystem
# Fully networked and touch enabled - with easy manipulation of generated maps
# Author: Matthew Timmons-Brown

# Import necessary libraries for control of different aspects
import socket
import math
import time
import sys
import subprocess
import threading
import random
# Import Kivy elements and tools that will be used for the user interface
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
# Import image manipulation tools
from PIL import Image, ImageDraw
# Import library that I have created to make communication and control easier
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
import serverxclient as serv

powerdown = ["sudo", "shutdown", "now"]

server = serv.Server()

# Set the distance and stepper connection to false (as have not connected)
distance = False
stepper = False
# Initialise distance and stepper connections, but IP addresses so far unknown
distance_connection = 0
stepper_connection = 0
# Set accuracy limit for sensor, any value above it will be rejected (mm)
accuracy_limit = 4000

class Communication(threading.Thread):
	"""A communication thread that connects to other subsystems in the background"""

	# Run method - automatically run when thread is started
	# Constantly waits for other two subsystems to come online, then changes to the main application page
	def run(self):
		self.setup()
		# While either of the subsystems are not connected
		while (distance == False) or (stepper == False):
			(connection, address) = self.awaiting_socket()
			print (connection, address)
			self.test_socket(connection)
		# Wait 2 seconds, then change to main screen
		time.sleep(2)
		application.current = "main"

	# Setup method
	# Sets up a server for subsystems to connect to
	def setup(self):
		server.setup_server()
		print "SUCCESS ON BIND"
	
	# Awaiting socket method
	# Waits for an incoming socket and then returns that socket's connection and address details
	def awaiting_socket(self):
		print "AWAITING"
		(connection, address) = server.socket_reception()
		return (connection, address)

	# Test socket
	# Identifies which subsystem the incoming connection is and changes global variables to indicate correct pairing
	def test_socket(self, connection):
		# Demands verification from subsystem
		server.send_data(connection,"VERIFY?")
		data_back = server.receive_data(connection)
		# If data_back is either subsystem, then change the Init screen labels from NO to OK!
		if data_back == "DISTANCE!":
			# set distance to OK
			application.current_screen.distance_on()
			# Update global variables with connection details
			global distance, distance_connection
			distance = True
			distance_connection = connection
		if data_back == "STEPPER!":
			# set stepper to OK
			application.current_screen.stepper_on()
			# Update global variables with connection details
			global stepper, stepper_connection
			stepper = True
			stepper_connection = connection
		print "Finished testing socket"

class InitScreen(Screen):
	"""A class to define the behaviour of the InitScreen"""

	# Power off method
	# If shutdown switch is toggled, turn off device
	def power_off(self, *args):
		# Connection to Kivy element through the use of labels
		onoffswitch = self.ids["onoffswitch"]
		onoff_value = onoffswitch.active
		# If the switch is false, turn the system off
		if onoff_value == False:
			subprocess.call(powerdown)
	
	# Distance ON! method
	# Changes the "NO" distance label to "OK!" when called
	def distance_on(self, *args):
		distance_label = self.ids["distance_label"]
		distance_label.text = "[size=40]Distance:[/size]\n\n[size=60][color=008000]OK[/color][/size]" # (Markup text)
	
	# Stepper ON! method
	# Changes the "NO" stepper label to "OK!" when called
	def stepper_on(self, *args):
		stepper_label = self.ids["stepper_label"]
		stepper_label.text = "[size=40]Stepper:[/size]\n\n[size=60][color=008000]OK[/color][/size]" # (Markup text)
				
class MainScreen(Screen):
	"""A class to define the behaviour of the MainScreen"""

	# Current stepper motor angle
	angle = 0	

	# Power off method
	# If shutdown switch is toggled, turn off other subsystems and shut down this device
	def power_off(self, *args):
		onoffswitch = self.ids["onoffswitch2"]
		onoff_value = onoffswitch.active
		if onoff_value == False:
			# Send commands to other subsystems and then shut down
			server.send_data(distance_connection, "POWER-OFF")
			server.send_data(stepper_connection, "POWER-OFF")
			subprocess.call(powerdown)

	# Change value method
	# When the slider is changed, adapt the value label to reflect its value
	def change_value(self, *args):
		value_slider = self.ids["value_slider"]
		self.angle = int(value_slider.value)
		value_label = self.ids["value_label"]
		# Change label to slider's current value
		value_label.text = "[size=10]" + str(self.angle) + "[/size]"
	
	# Scan method
	# Called when the SCAN button is pressed
	# Collects data from distance subsytem and stepper motor subsystem
	# Outputs map to the user
	def scan(self, *args):
		enable_lidar = self.ids["enable_lidar"]
		# If the lidar button is actually enabled, then proceed with the scan
		if enable_lidar.state == "down":
			print "Now contacting and getting data"
			# Create arrays for the distances and angle that they were recorded at
			distances = []
			positions = []

			# Create angle copy to reset when process has finished
			angle_copy = self.angle

			# For loop to discard the first 20 readings from the distance sensor
			# Sensor is cheap and found that the first 20 odd values are not usually consistent - so discard them
			for i in range(0,20):
				server.send_data(distance_connection, "FIRE")
				discarded_response = server.receive_data(distance_connection)
				time.sleep(0.1)

			# While there is still an angle left to scan, do:
			while self.angle+1.8 > 0:
				# Demand distance from distance subsystem
				server.send_data(distance_connection, "FIRE")
				distance_response = server.receive_data(distance_connection)

				# While the distance is greater than the accuracy limit, and the attempts are less than 3, try again
				# in the hope to get better data.
				tries = 0
				while (float(distance_response[:-2]) > accuracy_limit) and (tries < 3):
					server.send_data(distance_connection, "FIRE")
					distance_response = server.receive_data(distance_connection)
					tries += 1

				# Demand current position of stepper motor, and then rotate by 1 step for the next distance
				server.send_data(stepper_connection, "REPORT-ROTATE")
				stepper_position = server.receive_data(stepper_connection)
	
				# Convert the values into floats and remove unnecessary elements of communication
				point_distance = float(distance_response[:-2])
				point_position = float(stepper_position)

				print (point_position, point_distance)
				
				# If distance is within the accuracy_limit, store and record distance
				# Otherwise distance is not recorded. This is to prevent outliers
				if point_distance <= accuracy_limit:
					distances.append(point_distance)
					positions.append(point_position)

				# -1.8 from angle as scan complete
				self.angle -= 1.8

			# Reset current angle
			self.angle = angle_copy
			
			# Draw map with the distances and position data that has been gathered
			source = self.draw_map(distances, positions)
			# Display the outputted PNG image to the user for manipulation and viewing
			output_image = self.ids["output_image"]
			output_image.source = source
		else:
			print "Nothing enabled"

	# Draw map method
	# Main map drawing algorithm - creates image from supplied distances and position data and returns path to that image
	def draw_map(self, distance_array, angle_array):
		# Dimensions for the image
		dimensions = (700,380)
		points = len(distance_array)-1
		centre_x = dimensions[0]/2
		centre_y = dimensions[1]/2
		
		# Create a scaling factor for the end image to ensure points are within the allocated space
		scaler = (centre_x+accuracy_limit)/dimensions[0]
		# Open a new image with the dimensions previous
		map = Image.new("RGBA", dimensions)

		# Set image up for drawing
		draw = ImageDraw.Draw(map)
		# Draw a point in the centre of the image to represent where the scanner is
		draw.point((centre_x, centre_y), (1,1,1))

		# For all the pieces of data, do:
		for i in range(0, points):

			# Use trigonometry to calculate the position of the point to plot on map
			sine_distance = (math.sin(math.radians(angle_array[i]))*(distance_array[i]))
			cosi_distance = (math.cos(math.radians(angle_array[i]))*(distance_array[i]))
			
			length_x = cosi_distance
			length_y = sine_distance

			# Divide by scaling factor to keep within the dimensions of the image
			length_x = length_x/scaler
			length_y = length_y/scaler			
			
			# Create set of coordinates to plot
			coord_x = centre_x + length_x
			coord_y = centre_y + length_y

			coords = (coord_x, coord_y)
			print coords

			# Draw coordinates on map
			draw.point(coords, (1,1,1))

		# Create a new image path and return it
		path = "/home/pi/lidar/pi_approach/UI/scans/" + str(random.randint(0,1000)) + ".png"
		map.save(path, "PNG")
		return path
		

class ScreenManagement(ScreenManager):
	"""Screen Manager - does behind-the-scenes screen management for transition between Init and Main screen"""
	pass

# Load up Kivy file that defines how the UI looks
application = Builder.load_file("main.kv")

class LidarApp(App):
	"""Build actual application and return it"""
	def build(self):
		return application

# If run, start communication thread and run the application
if __name__ == "__main__":
	checker = Communication()
	checker.daemon = True
	checker.start()
	LidarApp().run()
