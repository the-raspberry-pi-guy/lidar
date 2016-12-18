/* arduino_distance
 * Uses VL53L0X Time-of-Flight Lidar sensor for distance measurement
 * Stepper motor rotation
 * Work in progress - Matthew Timmons-Brown
 */

#include <Wire.h>
#include <VL53L0X.h>

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
  int a;
  int lidar_array[3];
  populate_lidar_array(lidar_array);
  a = average_lidar_array(lidar_array);
  Serial.print(a);
  Serial.println();
}

int populate_lidar_array(int lidar_array[])
{
  int i;
  int len = sizeof(lidar_array);
  for (i = 0; i = (len-1); i = i +1)
  {
    lidar_array[i] = sensor.readRangeSingleMillimeters();
  }
}

int average_lidar_array(int lidar_array[])
{
  int i;
  int len = sizeof(lidar_array);
  int sum = 0;
  for (i = 0; i = (len-1); i = i + 1)
  {
    sum += lidar_array[i];  
  }
  int result;
  result = ((float) sum) / len;
  return result;
}
  
  

