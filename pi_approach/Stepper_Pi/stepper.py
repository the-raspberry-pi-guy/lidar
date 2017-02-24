# stepper.py
# Code to control the rotating stepper motor platform
# Networked to provide wireless setting and reporting
# Author: Matthew Timmons-Brown

# Import necessary libraries for control of different aspects
import time
import sys
import subprocess
sys.path.insert(0, "/home/pi/lidar/pi_approach/Libraries")
# Import libraries that I have created to make communication and control easier
import PicoBorgRev
import serverxclient as cli

powerdown = ["sudo", "shutdown", "now"]

# Create class instances for the motor and network
motor = PicoBorgRev.PicoBorgRev()
client = cli.Client()

class stepper_controller(object):
	""" An all-powerful stepper motor controller"""
	
	# Set class attributes
	current_step = -1
	power = 0.5 # Value of power to coils. 1 is full power
	motor_sequence = [[power, power], [power, -power], [-power, -power], [-power, power]] # Order for stepping and movement of motor
	step_delay = 0.002  # Delay between steps
	
	progress = 0
	degrees = 0

	# Init method - called when class initialised.
	# Prepares and initialises the stepper motor
	def __init__(self):
		motor.Init()
		motor.ResetEpo()
	
	# Handshake method
	# Attempts connection with the wireless user interface and verifies the subsystem
	def setup_handshake(self):
		connected = False
		# Repeat until connected
		while not connected:
			try:
				client.socket_connection()
				connected = True
			except:
				print "Failure"
				time.sleep(2)
		received_communication = client.receive_data()
		# Actual handshake process, awaiting verification message
		if received_communication == "VERIFY?":
			hand_shake = "STEPPER!"
			client.send_data(hand_shake)
		else:
			print "Unidentified communication"

	# Movement method
	# Called with number of steps as argument
	# Rotates the stepper motor by that number of steps
	def move_steps(self,count):
		# Reverse handling (if count is negative)
		if count < 0:
			dir = -1
			count *= -1
		else:
			dir = 1
					
		# While there are steps still remaining
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
        		
			# Update progress and degrees attributes with motor's current position
			self.progress += 1
			if self.progress > 200:
				self.progress -= 200
			self.degrees = self.progress*1.8
			time.sleep(stepper_controller.step_delay)
        		count -= 1
		
		motor.MotorsOff()

	# Active listen method
	# Waits for communication from the wireless user interface and then acts upon communication
	def active_listen(self):
		received_communication = client.receive_data()
		# Send position and rotate by 1
		if received_communication == "REPORT-ROTATE":
			result = self.degrees
			print result
			client.send_data(str(result))
			self.move_steps(1)
		# Power down
		if received_communication == "POWER-OFF":
			subprocess.call(powerdown)
			
	# Main method
	# Runs handshake and then forever runs active listening method
	def main(self):
		self.setup_handshake()
		while True:
			self.active_listen()

# Create class instance and run program	
if __name__ == "__main__":
	stepp = stepper_controller()
	stepp.main()
