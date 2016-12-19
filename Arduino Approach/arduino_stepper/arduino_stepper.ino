
/*
 Stepper Motor Control
 */

#include <Stepper.h>

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

int stepCount = 0;         // number of steps the motor has taken
int stepValue = 0;         // current step number the motor is on

void setup() {
  // initialize the serial port:
  Serial.begin(9600);
  myStepper.setSpeed(120);
}

void loop() {
  // step one step:
  myStepper.step(1);
  //Serial.print("steps:");
  //Serial.println(stepValue);
  //Serial.print("degrees: ");
  //Serial.println(stepCount*1.8);
  stepCount++;
  stepValue = stepCount + 1;
  if (stepValue > 200)
  {
    stepValue = stepValue - 200;
  }
}
