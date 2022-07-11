
#include <Wire.h> 
#include <Adafruit_Sensor.h> 
#include <Adafruit_BNO055.h> 
#include <utility/imumaths.h> 
#include "BluetoothSerial.h"
 
//For one I2C line in Parm’s tutorials we have -> data is blue and pin 21, clock is yellow and pin 22 
#define SDA_1 21 
#define SCL_1 22 
 
//here we define the pins for the other I2C line that you wired in part 1 of the tutorial 
#define SDA_2 19 
#define SCL_2 23 

BluetoothSerial SerialBT;
TwoWire I2Cone = TwoWire(0); 
TwoWire I2Ctwo = TwoWire(1); 


Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x28, &I2Cone); // pin 21 and 22
Adafruit_BNO055 bno2 = Adafruit_BNO055(55, 0x28, &I2Ctwo); // pin 19 and 20
 

void setup() { 
  Serial.begin(115200); 
  SerialBT.begin("ESP32test11111");
 
  //have I2C communication begin and tell I2Cone and I2Ctwo which lines are being used. 
  I2Cone.begin(SDA_1, SCL_1, 100000);  
  I2Ctwo.begin(SDA_2, SCL_2, 100000); 
 
  //check if you wired it correctly. If not you will constantly print what is below 
  bool status1 = bno1.begin();   
  if (!status1) { 
    Serial.println("Could not find a valid Bno_1 sensor, check wiring!"); 
    while (1); 
  } 
   
  bool status2 = bno2.begin();
    if (!status2) {
    Serial.println("Could not find a valid Bno_2 sensor, check wiring!");
    while (1);
  }
} 


void loop() {  

    if (SerialBT.available()) {
    
    /* Get a new sensor event */  
    sensors_event_t shank; 
    sensors_event_t thigh; 
    bno1.getEvent(&shank); 
    bno2.getEvent(&thigh); 
  
  
  
    SerialBT.print(thigh.orientation.z);
    //SerialBT.print(0);
    SerialBT.print(",");
    SerialBT.println(shank.orientation.z);
    delay(40);
    }
}

