# Touchscreen Kivy Interface for Lidar Project

import socket
import time
import sys
import subprocess
import threading
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
import serverxclient as serv

powerdown = ["sudo", "shutdown", "now"]

global distance
distance = False
stepper = False

class Communication(threading.Thread):
	server = serv.Server()

	def run(self):
		self.setup()
		while distance == False:
			(connection, address) = self.awaiting_socket()
			self.test_socket(connection)

	def setup(self):
		Communication.server.setup_server()
		print "SUCCESS ON BIND"
	
	def awaiting_socket(self):
		print "AWAITING"
		(connection, address) = Communication.server.socket_reception()
		return (connection, address)

	def test_socket(self, connection):
		Communication.server.send_data(connection,"VERIFY?")
		data_back = Communication.server.receive_data(connection)
		print data_back
		if data_back == "DISTANCE!":
			# set distance to OK
			print "Distance is OK"
			InitScreen.distance_on()
			global distance
			distance = True
		if data_back == "STEPPER!":
			# set stepper to OK
			print "Stepper is OK"

class DistanceStepperChecker(threading.Thread):
	def run(self):
		global distance
		if distance == True:
			print "TRIGGERED"
			distance_label = self.ids["distance_label"]
			distance_label.text = "[size=40]Distance:[/size]\n\n[size=60][color=008000]OK[/color][/size]"

class InitScreen(Screen):
	def power_off(self, *args):
		onoffswitch = self.ids["onoffswitch"]
		onoff_value = onoffswitch.active
		if onoff_value == False:
			subprocess.call(powerdown)
	
	def distance_on(self, *args):
		print "distance_on was triggered"
		distance_label = self.ids["distance_label"]
		distance_label.text = "[size=40]Distance:[/size]\n\n[size=60][color=008000]OK[/color][/size]"
		print distance_label.text	
	
#	while True:
#		if distance == True:
#			distance_label = self.ids["distance_label"]
#			distance_label.text = "[size=40]Distance:[/size]\n\n[size=60][color=008000]OK[/color][/size]"
				
class MainScreen(Screen):
	angle = 0	
	def change_value(self, *args):
		value_slider = self.ids["value_slider"]
		self.angle = int(value_slider.value)
		if self.angle == 361:
			self.angle = "CONT" 
		value_label = self.ids['value_label']
		value_label.text = "[size=10]" + str(self.angle) + "[/size]"
	
	def scan(self, *args):
		# Remember to add "if lidar/camera are on" 
		print self.angle
		# Scan through this angle

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
#	distance_checker = DistanceStepperChecker()
#	distance_checker.daemon = True
#	distance_checker.start()	
	LidarApp().run()
