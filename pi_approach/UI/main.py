# Touchscreen Kivy Interface for Lidar Project

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

#Window.clearcolor=(1,1,1,1)

class Init_Screen(GridLayout):
	pass

class Main_Screen(GridLayout):
	pass

class LidarApp(App):
	def build(self):
		return Main_Screen()

if __name__ == '__main__':
	LidarApp().run()
