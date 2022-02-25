//src from https://randomnerdtutorials.com/esp-now-many-to-one-esp32/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <WiFi.h>
#include <esp_now.h>
#define BNO055_SAMPLERATE_DELAY_MS (100)

// This is the sender ESP32 --> Slave 1410 usb right
Adafruit_BNO055 bno = Adafruit_BNO055(55);

// Contains receiver macAdress
//uint8_t broadcastAddress[] = {0xD8, 0xA0, 0x1D, 0x5F, 0xB6, 0xFC}; // Diane's
uint8_t broadcastAddress[] = {0x98, 0xCD, 0xAC, 0xF7, 0x8A, 0xD0}; // Chelsea
//98:CD:AC:F7:8A:D0 
typedef struct struct_message{
  int id;
  int x;
  int y;
  int z;
} struct_message;

// create a struct_message called myData
struct_message myData;

//Create peer interface
esp_now_peer_info_t peerInfo;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
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
  //98:CD:AC:F7:8A:D0 

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);

  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  Serial.println("Done Setup");
  
}



void loop() {

  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
    
  // Set values to send
  myData.id = 1;
  myData.x = euler.x();
  myData.y = euler.y();
  myData.z = euler.z();

  Serial.println(myData.z);
  
  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));

  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }
  delay(1000);
  
}

