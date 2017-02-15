# Pi Stepper
# Code to control the rotating stepper motor platform
# Work in progress - Matthew Timmons-Brown

import time
import sys
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
import PicoBorgRev
import serverxclient as cli

powerdown = ["sudo", "shutdown", "now"]

motor = PicoBorgRev.PicoBorgRev()
client = cli.Client()

class stepper_controller(object):
	""" An all-powerful stepper motor controller"""
	
	current_step = -1
	power = 0.5 # Power to coils
	motor_sequence = [[power, power], [power, -power], [-power, -power], [-power, power]] # Order for stepping
	step_delay = 0.002                                               # Delay between steps
	
	progress = 0
	degrees = 0

	def __init__(self):
		motor.Init()
		motor.ResetEpo()		

	def setup_handshake(self):
		connected = False
		while not connected:
			try:
				client.socket_connection()
				connected = True
			except:
				print "Failure"
				time.sleep(2)
		received_communication = client.receive_data()
		if received_communication == "VERIFY?":
			hand_shake = "STEPPER!"
			client.send_data(hand_shake)
		else:
			print "Unidentified communication"

	def move_steps(self,count):
		# data_list = []
		# Reverse handling
		if count < 0:
			dir = -1
			count *= -1
		else:
			dir = 1
					
		while (count > 0):
			data_list = []
			# If this is the first move, set starting position
		        if self.current_step == -1:
            			drive = self.motor_sequence[-1] # Access list from right
            			motor.SetMotor1(drive[0])
            			motor.SetMotor2(drive[1])
            			self.current_step = 0
        		else:
            			self.current_step += dir

			# Wrap step when end of sequence reached
	        	if self.current_step < 0:
        	    		self.current_step = len(stepper_controller.motor_sequence) - 1
        		elif self.current_step >= len(stepper_controller.motor_sequence):
            			self.current_step = 0

        		# For this step set the required drive values
        		if self.current_step < len(stepper_controller.motor_sequence):
            			drive = stepper_controller.motor_sequence[self.current_step]
            			motor.SetMotor1(drive[0])
            			motor.SetMotor2(drive[1])
        		
			self.progress += 1
			if self.progress > 200:
				self.progress -= 200
			self.degrees = str(self.progress*1.8)
			time.sleep(stepper_controller.step_delay)
        		count -= 1
		
		motor.MotorsOff()

	def active_listen(self):
		received_communication = client.receive_data()
		if received_communication == "REPORT-ROTATE":
			result = self.degrees
			client.send_data(str(result))
			self.move_steps(1)
		if received_communication == "POWER-OFF":
			subprocess.call(powerdown)
		else:
			print "ERROR"
	
	def main(self):
		self.setup_handshake()
		while True:
			self.active_listen()
		
stepp = stepper_controller()
stepp.main()
