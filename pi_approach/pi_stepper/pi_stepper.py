# Pi Stepper
# Code to control the rotating stepper motor platform
# Work in progress - Matthew Timmons-Brown

import PicoBorgRev
import time

motor = PicoBorgRev.PicoBorgRev()

class stepper_controller(object):
	""" An all-powerful stepper motor controller"""
	
	current_step = -1
	motor_sequence = [[1.0, 1.0], [1.0, -1.0], [-1.0, -1.0], [-1.0, 1.0]] # Order for stepping
	step_delay = 0.002                                               # Delay between steps


	def __init__(self):
		motor.Init()
		motor.ResetEpo()

	def move(self,count):
		# Reverse handling
		if count < 0:
			dir = -1
			count *= -1
		else:
			dir = 1
		
		while count > 0:
			# If this is the first move, set starting position
		        if stepper_controller.current_step == -1:
            			drive = stepper_controller.motor_sequence[-1] # Access list from right
            			motor.SetMotor1(drive[0])
            			motor.SetMotor2(drive[1])
            			stepper_controller.current_step = 0
        		else:
            			stepper_controller.current_step += dir

			# Wrap step when end of sequence reached
	        	if stepper_controller.current_step < 0:
        	    		stepper_controller.current_step = len(stepper_controller.motor_sequence) - 1
        		elif stepper_controller.current_step >= len(stepper_controller.motor_sequence):
            			stepper_controller.current_step = 0

        		# For this step set the required drive values
        		if stepper_controller.current_step < len(stepper_controller.motor_sequence):
            			drive = stepper_controller.motor_sequence[stepper_controller.current_step]
            			motor.SetMotor1(drive[0])
            			motor.SetMotor2(drive[1])
        		
			time.sleep(stepper_controller.step_delay)
        		count -= 1

	def main(self):
		try:
			motor.MotorsOff()
			while True:
				steps = input("Steps to move: ")
				stepper_controller.move(self, steps)
		except KeyboardInterrupt:
			motor.MotorsOff()

stepp = stepper_controller()
stepp.main()
