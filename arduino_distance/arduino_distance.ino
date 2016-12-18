/* arduino_distance
 * Uses VL53L0X Time-of-Flight Lidar sensor for distance measurement
 * Stepper motor rotation
 * Work in progress - Matthew Timmons-Brown
 */

#include <Wire.h>
#include <VL53L0X.h>
#define average_trials 3

VL53L0X sensor;

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
  int avg;
  int lidar_array[average_trials];
  populate_lidar_array(lidar_array);
  avg = average_lidar_array(lidar_array);
  Serial.print(avg);
  Serial.println();
}

int populate_lidar_array(int lidar_array[])
{
  for (int i = 0; i < average_trials; i = i +1)
  {
    lidar_array[i] = get_distance();
  }
}

int average_lidar_array(int lidar_array[])
{
  int sum = 0;
  for (int i = 0; i < average_trials; i = i + 1)
  {
    sum += lidar_array[i];  
  }
  int result;
  result = ((float) sum) / average_trials;
  return result;
}
  
int get_distance()
{
  return sensor.readRangeSingleMillimeters();
}

