/* arduino_distance
 * Uses VL53L0X Time-of-Flight Lidar sensor for distance measurement. Hand crafted averaging for greater precision
 * Stepper motor rotation. In progress.
 * Work in progress - Matthew Timmons-Brown
 */

// Import I2C and sensor library
#include <Wire.h>
#include <VL53L0X.h>

// Set a constant - number of trials before averaging
#define average_trials 3

// Initialise sensor
VL53L0X sensor;

// Setup loop
void setup()
{
  Serial.begin(9600);
  Wire.begin();
  sensor.init();
  sensor.setTimeout(500);
  sensor.setMeasurementTimingBudget(100000); // For higher accuracy measurement (up to 100ms)(value in microseconds)
}

void loop()
{
  // Initiliase variables
  int avg;
  int lidar_array[average_trials]; // Create array
  populate_lidar_array(lidar_array); // Pass array into populate_lidar_array function and fill with distance values
  avg = average_lidar_array(lidar_array); // Average array values and store in avg variable
  Serial.print(avg);
  Serial.println();
}

int populate_lidar_array(int lidar_array[])
{
  for (int i = 0; i < average_trials; i = i +1)
  {
    // For each index of the array, get distance and store distance at that index
    lidar_array[i] = get_distance();
  }
}

int average_lidar_array(int lidar_array[])
{
  int sum = 0;
  for (int i = 0; i < average_trials; i = i + 1)
  {
    // Sum each value in the array
    sum += lidar_array[i];  
  }
  int result; // Work out mean average and return result
  result = ((float) sum) / average_trials;
  return result;
}
  
int get_distance()
{
  // Get distance in millimeters from lidar sensor
  return sensor.readRangeSingleMillimeters();
}

