# Touchscreen Kivy Interface for Lidar Project

import socket
import sys
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
import serverxclient as serv

#Window.clearcolor=(1,1,1,1)

class Init_Screen(GridLayout):
	pass

class Main_Screen(GridLayout):

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

class LidarApp(App):
	def build(self):
		return Main_Screen()

if __name__ == "__main__":
	server = serv.Server()
	server.setup_server()
	(connection, address) = server.socket_reception()
	while True:
		print server.receive_data(connection)
	#LidarApp().run()
