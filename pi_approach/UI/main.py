# Touchscreen Kivy Interface for Lidar Project

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

#Window.clearcolor=(1,1,1,1)

class Init_Screen(GridLayout):
	pass

class Main_Screen(GridLayout):
	def change_value(self, *args):
		value_slider = self.ids['value_slider']
		new_value = value_slider.value
		value_label = self.ids['value_label']
		value_label.text = str(new_value)

class LidarApp(App):
	def build(self):
		return Main_Screen()

if __name__ == '__main__':
	LidarApp().run()
