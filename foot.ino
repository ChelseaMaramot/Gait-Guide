#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include "BluetoothSerial.h"
#define BNO055_SAMPLERATE_DELAY_MS (40) 

Adafruit_BNO055 bno = Adafruit_BNO055(55);
BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("Team32_foot_ESP32");
  Wire.begin(); 
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
    delay(1000);
}


void loop(){
  if (SerialBT.available()){
    imu::Vector<3> foot_accel = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
    imu::Vector<3> foot_angle = bno.getVector(Adafruit_BNO055::VECTOR_EULER); 
    SerialBT.print(foot_accel.y());
    SerialBT.print(",");
    SerialBT.println(foot_angle.z());

    delay(BNO055_SAMPLERATE_DELAY_MS);
    
  }
}