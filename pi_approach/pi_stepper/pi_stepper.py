# Pi Stepper
# Code to control the rotating stepper motor platform
# Work in progress - Matthew Timmons-Brown

import PicoBorgRev
import time

motor = PicoBorgRev.PicoBorgRev()

class stepper_controller(object):
	""" An all-powerful stepper motor controller"""
	
	current_step = -1
	power = 0.5 # Power to coils
	motor_sequence = [[power, power], [power, -power], [-power, -power], [-power, power]] # Order for stepping
	step_delay = 0.002                                               # Delay between steps
	
	progress = 0

	def __init__(self):
		motor.Init()
		motor.ResetEpo()

	def move_steps_transceive(self,count):
		# Reverse handling
		if count < 0:
			dir = -1
			count *= -1
		else:
			dir = 1
		
			
		while (count > 0):
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
            			drive = stepper_controller.motor_sequence[stepper_controller.current_step]
            			motor.SetMotor1(drive[0])
            			motor.SetMotor2(drive[1])
        		
			self.progress += 1
			degrees = self.progress*1.8

			# TRANSMIT POSITION DATA
			transmit(SOME PARAMETERS)

			time.sleep(stepper_controller.step_delay)
        		count -= 1
		
		motor.MotorsOff()

	def transmit(self):
		# TRANSMIT PARAMETERS
	
	def main(self):
		motor.MotorsOff()
		while True:
			if # receive #
				if # single rotation #
					steps = 200
					stepper_controller.move_steps_transceive(self, steps)
				if # cont rotation #
					cont = true
					while cont = true:
						stepper_controller.move_steps_transceive(self, 1)
						if # stop command #
							cont = false

stepp = stepper_controller()
stepp.main()
