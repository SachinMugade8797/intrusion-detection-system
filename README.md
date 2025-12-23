# Virtual Perimeter Intrusion Detection System

**Python | OpenCV | Real-Time Computer Vision**

## 📌 Overview

The **Virtual Perimeter Intrusion Detection System** is a real-time computer vision application built using Python and OpenCV. The system monitors a live video stream (webcam or video file), detects motion-based intrusions within a defined area, generates structured events, and stores them for further analysis.

---

## 🎯 Key Features

* Supports **both webcam and video file input**
* Real-time **motion detection using frame differencing & contour analysis**
* Intrusion event detection with **timestamp and intensity value**
* **FPS calculation** for performance monitoring
* **SQLite database storage** for detected events
* Modular and scalable project architecture
* Clean, readable, and maintainable codebase
  
---
### 🏗️ System Architecture
```
Input (Webcam / Video File)
        ↓
Frame Processing (Grayscale + Blur)
        ↓
Motion Detection (Frame Differencing)
        ↓
Contour Detection
        ↓
Intrusion Logic (Perimeter Crossing)
        ↓
Event Generation
        ↓
REST API (Flask)
        ↓
SQLite Database
```
---

## 🔄 End-to-End Workflow

1. Capture frames from **webcam or video file**
2. Convert frames to grayscale and detect motion
3. Extract contours and analyze motion intensity
4. Apply intrusion detection logic
5. Generate structured intrusion events
6. Store events in SQLite database
7. Send events to backend interface


---

## 🏗️ Project Architecture

```
intrusion-detection-system/
│
├── backend/
│   └── api.py                 # Event communication layer (API/WebSocket ready)
│
├── camera/
│   └── video_stream.py        # Webcam / video file handler
│
├── config/
│   └── settings.py            # Centralized configuration
│
├── processing/
│   ├── motion_detector.py     # Motion detection logic
│   ├── intrusion_logic.py     # Intrusion decision rules
│   └── contour_utils.py       # Contour utilities
│
├── storage/
│   └── database.py            # SQLite event storage
│
├── utils/
│   ├── event.py               # Event data structure
│   └── fps.py                 # FPS calculation utility
│
├── data/
│   └── events.db              # Stored intrusion events
│
├── requirements.txt
└── main.py                    # Application entry point
```


---
## 📷 Video Input Support

The system works with:

* **Webcam input**
* **Pre-recorded video files**

This makes the project suitable for both **real-time monitoring** and **testing/demo purposes**.


# Project Start
<img width="1605" height="941" alt="Screenshot 2025-12-23 002817" src="https://github.com/user-attachments/assets/25010c11-ebd9-4b05-9df6-dbbd48d6281e" />

---

## 🧠 Event Detection Logic

An intrusion event is triggered when:

* Motion exceeds a predefined threshold
* Contour area crosses the configured limit

Each event includes:

* `timestamp`
* `event_type` (e.g., intrusion_detected)
* `event_value` (motion intensity / contour area)

  
# After Crossing Line
<img width="1618" height="956" alt="Screenshot 2025-12-23 002849" src="https://github.com/user-attachments/assets/af78b799-b32a-4cbf-a195-31b0b24d4acf" />


---

## 🗄️ Data Storage

* Uses **SQLite** for lightweight and reliable storage
* Stores:

  * Timestamp
  * Event type
  * Event value
* Easily extendable to PostgreSQL or cloud databases
# Database Stored Information
<img width="1891" height="969" alt="Screenshot 2025-12-23 003657" src="https://github.com/user-attachments/assets/751a3bf4-b9b4-408f-b981-d7de07fe7da1" />



---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SachinMugade8797/intrusion-detection-system
cd intrusion-detection-system
```

### 2️⃣ Create Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Video Source

Edit `config/settings.py`:

```python
VIDEO_SOURCE = 0          # Webcam
# or
VIDEO_SOURCE = "video.mp4"
```

### 5️⃣ Run the Application

```bash
python main.py
```

---

## 🚀 Bonus Features Implemented

* FPS calculation and display
* Modular processing pipeline
* Easy backend integration support
* Clean separation of concerns

---
## 🔍 Assumptions

#### This system is developed based on the following assumptions:
* The camera remains fixed and stable (no camera shake).
* The environment has sufficient lighting for motion detection.
* Objects crossing the perimeter are large enough to exceed the minimum contour area.
* Only one video source (webcam or video file) is processed at a time.
* The virtual perimeter is defined as a single straight line.
* Intrusion detection is based on motion, not object identity.
* SQLite is used for local storage and demonstration purposes.
* The system is designed for basic intrusion detection, not high-security production use.

---

## 🧪 Example Use Case

Imagine a camera watching a restricted area.
When someone walks into the frame:

* The system notices movement
* Detects unusual motion
* Triggers an intrusion event
* Saves the event details automatically

This makes it a **clear and easy-to-understand example** of a virtual security perimeter.

---

## 🚀 Future Improvements

* The system can be enhanced in the following ways:
* Support for multiple perimeter lines or polygon-based restricted zones.
* Integration of object detection models (e.g., YOLO) to classify humans, vehicles, etc.
* Use WebSockets instead of REST API for real-time event streaming.
* Add object tracking to avoid duplicate intrusion events.
* Enable multi-camera support with centralized monitoring.
* Improve detection accuracy in low-light or noisy environments.
* Develop a web-based dashboard to visualize live feed and intrusion logs.
* Migrate database to PostgreSQL or cloud storage for scalability.
* Add alert notifications (email, SMS, or push notifications).

---

## 👤 Author

**Sachin Mugade**
Python & Computer Vision Developer

---
