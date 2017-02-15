# Touchscreen Kivy Interface for Lidar Project

import socket
import math
import time
import sys
import subprocess
import threading
import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
import serverxclient as serv

powerdown = ["sudo", "shutdown", "now"]

server = serv.Server()

distance = False
stepper = False
distance_connection = 0
stepper_connection = 0
accuracy_limit = 5000

class Communication(threading.Thread):
	def run(self):
		self.setup()
		while (distance == False) or (stepper == False):
			(connection, address) = self.awaiting_socket()
			print (connection, address)
			self.test_socket(connection)
		time.sleep(2)
		application.current = "main"

	def setup(self):
		server.setup_server()
		print "SUCCESS ON BIND"
	
	def awaiting_socket(self):
		print "AWAITING"
		(connection, address) = server.socket_reception()
		return (connection, address)

	def test_socket(self, connection):
		server.send_data(connection,"VERIFY?")
		data_back = server.receive_data(connection)
		print data_back
		if data_back == "DISTANCE!":
			# set distance to OK
			application.current_screen.distance_on()
			global distance, distance_connection
			distance = True
			distance_connection = connection
		if data_back == "STEPPER!":
			# set stepper to OK
			application.current_screen.stepper_on()
			global stepper, stepper_connection
			stepper = True
			stepper_connection = connection
		print "Finished testing socket"

class InitScreen(Screen):
	def power_off(self, *args):
		onoffswitch = self.ids["onoffswitch"]
		onoff_value = onoffswitch.active
		if onoff_value == False:
			subprocess.call(powerdown)
	
	def distance_on(self, *args):
		distance_label = self.ids["distance_label"]
		distance_label.text = "[size=40]Distance:[/size]\n\n[size=60][color=008000]OK[/color][/size]"
	
	def stepper_on(self, *args):
		stepper_label = self.ids["stepper_label"]
		stepper_label.text = "[size=40]Stepper:[/size]\n\n[size=60][color=008000]OK[/color][/size]"
				
class MainScreen(Screen):
	angle = 0	
	distances = []
	positions = []

	def power_off(self, *args):
		onoffswitch = self.ids["onoffswitch2"]
		onoff_value = onoffswitch.active
		if onoff_value == False:
			server.send_data(distance_connection, "POWER-OFF")
			server.send_data(stepper_connection, "POWER-OFF")
			subprocess.call(powerdown)

	def change_value(self, *args):
		value_slider = self.ids["value_slider"]
		self.angle = int(value_slider.value)
		value_label = self.ids["value_label"]
		value_label.text = "[size=10]" + str(self.angle) + "[/size]"
	
	def scan(self, *args):
		# Remember to add "if lidar/camera are on"
		enable_lidar = self.ids["enable_lidar"]
		if enable_lidar.state == "down":
			print "Now contacting and getting data"
			self.distances = []
			self.positions = []
			angle_copy = self.angle

			for i in range(0,9):
				server.send_data(distance_connection, "FIRE")
				discarded_response = server.receive_data(distance_connection)
				time.sleep(0.05)

			while self.angle+1.8 > 0:
				server.send_data(distance_connection, "FIRE")
				distance_response = server.receive_data(distance_connection)
				tries = 0
				while (float(distance_response[:-2]) > accuracy_limit) and (tries < 3):
					server.send_data(distance_connection, "FIRE")
					distance_response = server.receive_data(distance_connection)
					tries += 1

				server.send_data(stepper_connection, "REPORT-ROTATE")
				stepper_position = server.receive_data(stepper_connection)
	
				point_distance = float(distance_response[:-2])
				point_position = float(stepper_position)

				if point_distance > accuracy_limit:
					point_distance = 0

				self.distances.append(point_distance)
				self.positions.append(point_position)

				self.angle -= 1.8

			self.angle = angle_copy
			print self.distances
			print self.positions
			source = self.draw_map(self.distances, self.positions)
			output_image = self.ids["output_image"]
			output_image.source = source
		else:
			print "Nothing enabled"

	def draw_map(self, distance_array, angle_array):
		end_dimensions = (700,380)
		points = len(distance_array)-1
		highest_val = 0
		for i in range(0,points):
                	if distance_array[i] > highest_val:
				highest_val = distance_array[i]
		
		dimensions = (int(highest_val)+(2*end_dimensions[0]),int(highest_val)+(2*end_dimensions[1]))
		centre_x = dimensions[0]/2
		centre_y = dimensions[1]/2
		map = Image.new("RGBA", dimensions)
		line = []

		draw = ImageDraw.Draw(map)
		for i in range(0, points):
			if angle_array[i] == 0:
				angle_array[i] = 0.01
			sine = math.sin(math.radians(angle_array[i]))
			cosi = math.cos(math.radians(angle_array[i]))
			if sine == 0:
				sine = 1
			length_y = sine*distance_array[i]
			length_x = cosi*distance_array[i]

								
			coord_x = centre_x + length_x
			if coord_x > dimensions[0]:
				coord_x = dimensions[0]
			if coord_x < 0:
				coord_x = 0

			coord_y = centre_y + length_y
			if coord_y > dimensions[1]:
				coord_y = dimensions[1]
			if coord_y < 0:
				coord_y = 0

			coords = (coord_x, coord_y)
			print coords
			line.append(coords)

		if highest_val > 1000:
			pen_size = 10
		else:
			pen_size = 5

		draw.line(line,(1,1,1), pen_size)

		map = map.resize(end_dimensions, Image.ANTIALIAS)
		path = "/home/pi/lidar/pi_approach/UI/scans/" + str(random.randint(0,1000)) + ".png"
		print path
		map.save(path, "PNG")
		return path
		

class ScreenManagement(ScreenManager):
	pass

application = Builder.load_file("main.kv")

class LidarApp(App):
	def build(self):
		return application

if __name__ == "__main__":
	checker = Communication()
	checker.daemon = True
	checker.start()
	LidarApp().run()
