import serial

arduino_dist = serial.Serial('/dev/ttyUSB0',9600)

def get_distance():
	distance = arduino_dist.readline()
	return distance

print(get_distance())
