import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class App(App):
	def build(self):
		b = BoxLayout(orientation='vertical')
		t = TextInput(font_size = 150,size_hint_y=None, height = 200)
		l = Label(text="Hello", font_size = 150)
		f = FloatLayout()
        	s = Scatter()
		
		t.bind(text=function)		

		f.add_widget(s)
		s.add_widget(l)
		b.add_widget(t)
		b.add_widget(f)
				
		return b
		
def function():
	print

App().run()
