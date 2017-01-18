# Touchscreen Kivy Interface for Lidar Project

from kivy.app import App
from kivy.uix.widget import Widget

class Init_Screen(Widget):
    pass

class LidarApp(App):
    def build(self):
        return Init_Screen()

if __name__ == '__main__':
    LidarApp().run()
