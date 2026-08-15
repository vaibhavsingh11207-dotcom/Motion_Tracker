AI-powered real-time human tracking camera using YOLOv8, ESP32, and a custom pan-tilt mechanism. 


# 🤖 AI-Based Motion Tracking Pan-Tilt Camera Stand

A DIY AI-powered pan-and-tilt camera stand built using an **ESP32, servo motors, computer vision, and a custom-designed mechanical platform**.

The system uses a camera connected to a laptop to detect and track a person in real time. The detected position is sent to an ESP32, which controls two servo motors to rotate the camera horizontally and vertically, keeping the subject approximately centered in the frame.

This project was built from scratch as a hands-on exploration of **computer vision, robotics, embedded systems, and mechanical design**.




## ✨ Features

* Real-time human detection using **YOLO**
* Automatic horizontal (**pan**) tracking
* Automatic vertical (**tilt**) tracking
* ESP32-based servo control
* Custom-designed pan-and-tilt mechanism
* CAD model created in **Tinkercad**
* Computer vision running on a laptop
* Serial communication between Python and ESP32
* Physical prototype built using inexpensive materials


## 🧠 How It Works

The project consists of two main systems: the **computer vision system** and the **pan-tilt control system**.

### 1. Computer Vision

A webcam connected to the laptop captures live video.

The Python program uses **YOLO** to detect a person and determine the center coordinates of the detected bounding box.

These coordinates are then sent to the ESP32 through serial communication.


Camera
   ↓
Python + YOLO
   ↓
Person Detection
   ↓
Center X / Center Y Coordinates
   ↓
Serial Communication
   ↓
ESP32


## 🧩 CAD Design


The pan-and-tilt mechanism was designed in Tinkercad before being constructed physically.


### 🔧 Assembly Instructions

The arrows in the CAD model indicate the following:

**1st Arrow — Pan Servo:**
The first arrow shows the position of the **pan servo**. The servo should be attached so that its rotating horn can rotate the upper part of the platform, allowing the camera to **pan left and right**.

**2nd Arrow — Tilt Servo:**
The second arrow represents the position of the **tilt servo**. The servo is connected between the lower and upper parts of the platform so that its movement allows the upper platform to **tilt up and down**.

If the servo is unable to handle the weight of the upper platform or the mechanism becomes unbalanced, the servo horn can be extended by attaching longer sticks to it. This provides additional leverage for the tilt mechanism.

**3rd & 4th Arrows — Required Screws:**
The third and fourth arrows indicate the locations where **screws are necessary** to secure the mechanical joints of the platform.

> **Note:** The CAD model is intended as a reference for the physical construction. Some dimensions or structural details may need to be adjusted depending on the materials, servo positioning, and weight of the camera being used.

(these info is valid for the image below) . ![Pan and Tilt Platform](./pan%20and%20tilt%20platform%20labels%20.png)




### 2. Pan-Tilt Control

The ESP32 receives the detected coordinates and compares them with the center of the camera frame.

Depending on the person's position:

* Moving left/right → the **pan servo** adjusts.
* Moving up/down → the **tilt servo** adjusts.
* When the person is approximately centered → the servos stop adjusting.
  
   A[📷 USB Webcam] --> B[💻 Python + YOLOv8]
   B --> C[👤 Detect Person]
   C --> D[📍 Calculate Center X, Y]
   D --> E[🔌 Serial Communication]
   E --> F[⚙️ ESP32]

   F --> G[↔️ Pan Servo]
   F --> H[↕️ Tilt Servo]

   G --> I[Pan Movement]
   H --> J[Tilt Movement]

   I --> K[🎥 Pan-Tilt Camera]
   J --> K



## 🔩 Hardware

| Component              | Purpose                        |
| ---------------------- | ------------------------------ |
| ESP32                  | Controls the servo motors      |
| 2× MG90S Servo Motors  | Pan and tilt movement          |
| USB Webcam             | Captures video                 |
| Laptop                 | Runs the computer vision model |
| Ice cream sticks       | Mechanical structure           |
| Jumper wires           | Electrical connections         |
| 5V power supply        | Powers the servos              |
| Custom mounting pieces | Holds the camera and servos    |

The mechanical platform was manually constructed and adapted during assembly to account for the weight of the camera and the available servo torque.



## 💻 Software

* **Python**
* **OpenCV**
* **Ultralytics YOLO**
* **Arduino IDE**
* **ESP32Servo**
* **PySerial**
* **Tinkercad** — mechanical/CAD design
* **Serial communication*


## 📁 Project Structure


Motion_Tracker

─ README.md
─ motion tracker.py
─ probablyfinalcode.ino
─ tinker.obj

─ pan and tilt platform labels .png
─ backside of pan and tilt platform.png



*Filenames may differ depending on the final repository organization.*


## ⚙️ Pin Configuration

| Function   | ESP32 GPIO |
| ---------- | ---------: |
| Pan Servo  |    GPIO 19 |
| Tilt Servo |    GPIO 18 |

The servos operate using a standard **50 Hz PWM signal**.



## 🚀 Setup

### 1. Install Python Dependencies


pip install ultralytics opencv-python pyserial


### 2. Upload the ESP32 Code

Open:


esp32/servo_control.ino


Select the appropriate ESP32 board and upload the program using Arduino IDE.

### 3. Connect the Webcam

Connect the USB webcam to the laptop.

### 4. Start the Python Program

Run:


python motion_tracking.py


The program detects the person and sends their position to the ESP32.



## 🔄 Tracking Logic

The camera frame is divided into tracking regions.


        CAMERA FRAME

     ┌─────────────────┐
     │                 │
     │       ↑         │
     │       │         │
     │   ←  PERSON  →  │
     │       │         │
     │       ↓         │
     │                 │
     └─────────────────┘


A small center region acts as a **dead zone**, preventing unnecessary servo movement when the subject is already approximately centered.



## 🛠️ Development Process

The project was developed through multiple iterations of both software and hardware.

Some of the challenges encountered included:

* ESP32 programming and upload issues
* Servo power and wiring problems
* Mechanical instability
* Servo torque limitations
* Camera weight affecting the tilt mechanism
* Designing the pan mechanism
* Adjusting the pan/tilt geometry
* Mounting the servos securely
* Tuning the tracking behavior
* Adapting the CAD design into a physical prototype

The final system was achieved through **testing, debugging, redesigning, and rebuilding** rather than following a fixed construction plan.


## 🧪 What I Learned

This project gave me hands-on experience across several areas of engineering.

### 👁️ Computer Vision

* Object detection
* Bounding boxes
* Object center coordinates
* Real-time camera processing
* YOLO

### ⚡ Embedded Systems

* ESP32 programming
* GPIO
* PWM
* Servo motors
* Serial communication

### 🤖 Robotics

* Pan-tilt mechanisms
* Servo positioning
* Torque considerations
* Mechanical stability
* Hardware/software integration

### 🔧 Mechanical Design

* CAD modeling
* Designing mechanical joints
* Structural reinforcement
* Prototyping
* Translating a digital model into a physical mechanism

Most importantly, I learned that **making individual parts work is very different from making an entire real-world system work**.

The software, electronics, and mechanical structure all have to work together.



## 🔮 Future Improvements

Possible improvements for future versions include:

* 3D-printed mechanical parts
* Bearings for smoother rotation
* Stronger/higher-torque servos
* Dedicated camera module
* Wireless communication
* Smoother servo control
* PID-based tracking
* Faster tracking response
* Battery-powered operation
* More compact electronics
* Autonomous tracking without a laptop


## 🏁 Final Result

A fully functional DIY camera tracking system capable of detecting and following a person using computer vision and a custom-built pan-tilt mechanism.

The project combines **AI, computer vision, embedded programming, robotics, CAD, and mechanical prototyping** into a single working system.

Built using inexpensive and easily available materials.

**From a CAD model to an ice-cream-stick prototype to a working AI motion-tracking robot. 🤖**



## 👨‍💻 Author

**Vaibhav Singh**

A personal project exploring **AI, robotics, computer vision, embedded systems, and mechanical design**.



## 📜 License

This project is available for educational and personal use.

Feel free to experiment with the design, modify the code, and build upon the project.
