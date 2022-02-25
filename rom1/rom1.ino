//src from https://randomnerdtutorials.com/esp-now-many-to-one-esp32/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <WiFi.h>
#include <esp_now.h>
#define BNO055_SAMPLERATE_DELAY_MS (100)
  
Adafruit_BNO055 bno = Adafruit_BNO055(55);


// This is the receiver ESP32 --> Master 1420 usb left


// Must match the sender structure
typedef struct struct_message {
  int id;
  int x;
  int y;
  int z;
}struct_message;

// Create a struct_message called myData
struct_message myData;

// Create a structure to hold the readings from each board
struct_message board1;

// Create an array with all the structures
struct_message boardsStruct[1] = {board1};

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac_addr, const uint8_t *incomingData, int len) {

  // get board macAdress
  char macStr[18];
  //Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  //Serial.println(macStr);

  
  memcpy(&myData, incomingData, sizeof(myData));
  //Serial.printf("Board ID %u: %u bytes\n", myData.id, len);
  // Update the structures with the new incoming data
  boardsStruct[myData.id-1].x = myData.x;
  boardsStruct[myData.id-1].y = myData.y;
  boardsStruct[myData.id-1].z = myData.z;
  Serial.printf("shank %d ", boardsStruct[myData.id-1].x);
  Serial.printf(" %d ", boardsStruct[myData.id-1].y);
  Serial.printf(" %d ", boardsStruct[myData.id-1].z);
  Serial.println();
}


void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
  
}

void displaySensorStatus(void)
{
  /* Get the system status values (mostly for debugging purposes) */
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  /* Display the results in the Serial Monitor */
  Serial.println("");
  Serial.print("System Status: 0x");
  Serial.println(system_status, HEX);
  Serial.print("Self Test:     0x");
  Serial.println(self_test_results, HEX);
  Serial.print("System Error:  0x");
  Serial.println(system_error, HEX);
  Serial.println("");
  delay(100);

}

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
Serial.println("Orientation Sensor Test"); Serial.println("");
Wire.begin(); 
if(!bno.begin())
{
  /* There was a problem detecting the BNO055 ... check your connections */
  Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
  while(1);
}
  delay(1000);

  /* Display some basic information on this sensor */
  displaySensorDetails();

  /* Optional: Display current status */
  displaySensorStatus();

  bno.setExtCrystalUse(true);
  
  Serial.println(WiFi.macAddress());
  //D8:A0:1D:5F:B6:FC


  //Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  //Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);
  
}

int calculate_knee_angle(int thigh_y, int shank_z){
  // Thigh Y value located on the side of the thigh
  // Shank Z value located on the front of the shank

  //Serial.print("Thigh: "); Serial.print(thigh_y);
  //Serial.println("\nShank: "); Serial.print(shank_z);
  //Serial.println();


  //return thigh_y * -1 - (shank_z + 90)*-1;
  return (thigh_y * - shank_z - 90) *-1;
}

void loop() {
  
  // Access the variables for each board --> shank
  int board1X = boardsStruct[0].x;
  int board1Y = boardsStruct[0].y;
  int board1Z = boardsStruct[0].z;

  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

  Serial.print("knee joint angle: "); Serial.print(calculate_knee_angle(euler.y(), board1Z));
  Serial.println();

  //  thigh angles
  Serial.print("\nthigh: "); Serial.print(euler.x());
  Serial.print(" "); Serial.print(euler.y());
  Serial.print(" "); Serial.print(euler.z());
  Serial.println();

  delay(1000);
}