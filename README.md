# Gait-Guide

Gait-Guide allows total knee arthroplasty (TKR) to remotely monitor knee range of motion (ROM) during walking gait.

Outcomes measured (associated sensors):

* Knee Flexion/Extension (gyroscope)
* Stride Length (gyroscope)
* Walking Speed (accelerometer)
* Stance and Swing Time

Data will be presented using a Graphical User Interface designed using Tkinter. GUI displays a live graph of the user's knee flexion, along with the options to graph a normative data and previous user data. Collected data is stored and average is graphed to track user recovery and progress.


## Set Up

### Materials

* 3D printed housing units for sensors and arduino
* 3 BNO055 sensors
* 2 ESP32-PICO-D4 series Transceiver
* Jumper Wires (M-F, F-F, M-M)
* 2 Breadboard
* 2 USB 2.0 Power Cable
* 2 QWIIC Cable
* Portable Charger
* Leg Brace

### Board Schematics

![board_schematic](https://user-images.githubusercontent.com/61253723/178176226-47346ba3-673a-4570-969f-5e46e9355220.png)

![esp32_set_up](https://user-images.githubusercontent.com/61253723/178176296-867a575e-5040-4c5d-b7a6-7a64564d2679.png)


### Software
![output_data](https://user-images.githubusercontent.com/61253723/178176381-883d76dc-d6b5-4252-a61e-3023f87879a5.png)

* The arduino scripts (knee.ino and foot.ino) are ran to acquire data from the sensors. The acquired data is transferred to be used in the Python scripts. This is done through a bluetooth connection.
* The sensors are programmed to calibrate according to its placement on the user's leg and foot. This is done by subtracting an average offset in the angles collected. To begin calibration, press start on the GUI. The user must stand still, until a graph appears on the GUI to indicate that the user can begin movement.
  * Previous: allows the user to graph their grate alongside previous data.
  * Current: allows the user to graph only the acquired gait data.
  * Online: allows the user to graph their gate alongside normative data.

Note: All data is graphed live, as the user walks. 


### Physical Prototype
![prototype_front](https://user-images.githubusercontent.com/61253723/178178442-02c581d3-5e11-4baf-8f58-74fcf48b454b.jpg)


![prototype_side](https://user-images.githubusercontent.com/61253723/178176885-7ae03b0e-3a55-4be0-8665-a701957fc469.jpg)

The final prototype is a leg brace and a shoe band. Leg brace sensors are placed laterally, while shoe band is placed anterior.


