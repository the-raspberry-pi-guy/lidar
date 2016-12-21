#!/usr/bin/env python
# coding: latin-1

# Import library functions we need
import PicoBorgRev
import time

# Tell the system how to drive the stepper
power = 0.5
sequence = [[power, power], [power, -power], [-power, -power], [-power, power]] # Order for stepping 
stepDelay = 0.002                                               # Delay between steps

# Name the global variables
global step
global PBR

# Setup the PicoBorg Reverse
PBR = PicoBorgRev.PicoBorgRev()
#PBR.i2cAddress = 0x44                   # Uncomment and change the value if you have changed the board address
PBR.Init()
PBR.ResetEpo()
step = -1

# Function to perform a sequence of steps as fast as allowed
def MoveStep(count):
    global step
    global PBR

    # Choose direction based on sign (+/-)
    if count < 0:
        dir = -1
        count *= -1
    else:
        dir = 1

    # Loop through the steps
    while count > 0:
        # Set a starting position if this is the first move
        if step == -1:
            drive = sequence[-1]
            PBR.SetMotor1(drive[0])
            PBR.SetMotor2(drive[1])
            step = 0
        else:
            step += dir

        # Wrap step when we reach the end of the sequence
        if step < 0:
            step = len(sequence) - 1
        elif step >= len(sequence):
            step = 0

        # For this step set the required drive values
        if step < len(sequence):
            drive = sequence[step]
            PBR.SetMotor1(drive[0])
            PBR.SetMotor2(drive[1])
        time.sleep(stepDelay)
        count -= 1

try:
    # Start by turning all drives off
    PBR.MotorsOff()
    # Loop forever
    while True:
        # Ask the user how many steps to move
        steps = input("Steps to move (-ve for reverse, 0 to quit): ")
        if steps == 0:
            # Turn off the drives and release the GPIO pins
            PBR.MotorsOff()
            print 'Goodbye'
            break
        else:
            # Move the specified amount of steps
            MoveStep(steps)
except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    PBR.MotorsOff()
    print 'Terminated'

