# Pi Stepper
# Code to control the rotating stepper motor platform
# Work in progress - Matthew Timmons-Brown

import PicoBorgRev
import time

motor = PicoBorgRev.PicoBorgRev()

class stepper(object):
	""" An all-powerful stepper motor controller"""
	
	step = -1
	sequence = [[1.0, 1.0], [1.0, -1.0], [-1.0, -1.0], [-1.0, 1.0]] # Order for stepping
	stepDelay = 0.002                                               # Delay between steps


	def __init__(self):
		motor.Init()
		motor.ResetEpo()

	def move(self,count):
		if count < 0:
			dir = -1
			count *= -1
		else:
			dir = 1
		
		while count > 0:
			# Set a starting position if this is the first move
		        if stepper.step == -1:
            			drive = stepper.sequence[-1]
            			motor.SetMotor1(drive[0])
            			motor.SetMotor2(drive[1])
            			stepper.step = 0
        		else:
            			stepper.step += dir

			# Wrap step when we reach the end of the sequence
	        	if stepper.step < 0:
        	    		stepper.step = len(stepper.sequence) - 1
        		elif stepper.step >= len(stepper.sequence):
            			stepper.step = 0

        		# For this step set the required drive values
        		if stepper.step < len(stepper.sequence):
            			drive = stepper.sequence[stepper.step]
            			motor.SetMotor1(drive[0])
            			motor.SetMotor2(drive[1])
        		
			time.sleep(stepper.stepDelay)
        		count -= 1

	def main(self):
		try:
			motor.MotorsOff()
			while True:
				stepper.steps = input("Steps to move: ")
				stepper.move(self, stepper.steps)
		except KeyboardInterrupt:
			motor.MotorsOff()

stepp = stepper()
stepp.main()
