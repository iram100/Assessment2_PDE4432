

#  PDE4446- Vision-Based Pan–Tilt Object Tracking System

### *Robot Control & Sensing using OpenCV*

---
##  GitHub Repository

 https://github.com/iram100/Assessment2_PDE4432

 ##  Project Demonstration Video

A full demonstration of the system, including object tracking, multi-colour detection, and eye-colour estimation, is available on YouTube:

https://youtu.be/OTWWRsuRx70?si=Xj3jnyYB-KSWy3jf


## 1. Project Overview

This project implements a **real-time vision-based tracking system** using a camera mounted on a **pan–tilt servo mechanism**. The system detects a coloured object (red cube/ball) using **OpenCV**, estimates its position in the image plane, and generates smooth control commands to align the camera with the object.

The project follows a **modular robotics pipeline**:

> **Sensing → Perception → State Estimation → Control → Actuation**

In addition to basic object tracking, the system integrates **advanced computer vision and signal processing techniques**, including **HSV colour segmentation**, **morphological filtering**, **Kalman filtering**, **multi-colour tracking**, and **face & eye colour detection**.

---

## 2. Hardware Setup

* USB Camera
* Arduino-controlled pan–tilt servo mount
* Computer running Python (OpenCV)
* Serial communication between Python and Arduino

The Arduino expects **absolute pan and tilt commands** in the range **–1 to +1**, corresponding to normalized servo positions.

---

## 3. Software Environment

### Libraries Used

* **OpenCV** – image processing & computer vision
* **NumPy** – numerical computation
* **PySerial** – serial communication

Install dependencies using:

```bash
pip install opencv-python numpy pyserial
```

---

## 4. Project Structure 

```
Project/
│
├── Auto_Tracking_final.py        # Final integrated tracking system
├── Kalman_Tracking.py            # Kalman filter implementation
├── multi_color_tracker.py        # Multi-colour tracking logic
├── Eye_color_tracking.py         # Face, eye & eye-colour detection
│
├── Contour_Testing.py            # Contour debugging & validation
├── contour_compact_debug.py      # Compact contour scoring experiments
│
├── hsv_tuning.py                 # Interactive HSV tuning tool
├── hsv_values.json               # Saved HSV threshold values
│
├── servo_control_Manual.py       # Manual pan–tilt testing
├── camera_KeepAlive.py           # Camera stability testing
├── Testing_Camera.py             # Camera initialization checks
│
├── __pycache__/
└── .venv/
```

This structure reflects **incremental development**, where each subsystem was tested independently before full integration.

---

## 5. Computer Vision Pipeline (OpenCV Concepts Used)

### 5.1 Camera Acquisition

* `cv2.VideoCapture`
* Frame resolution configuration
* Horizontal frame flipping for intuitive control

Purpose:

> Validate camera reliability before adding control logic.

---

### 5.2 Colour Space Conversion (HSV)

The system uses the **HSV colour space** instead of RGB because:

* Hue isolates colour information
* Saturation & value handle illumination changes better

```python
cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

HSV thresholds are tuned interactively using `hsv_tuning.py` and saved in `hsv_values.json`.

---

### 5.3 Colour Segmentation

Binary masks are generated using:

```python
cv2.inRange(hsv, lower, upper)
```

For red objects, **dual HSV ranges** are used to handle hue wraparound (0° / 180°).

---

### 5.4 Morphological Filtering

To remove noise and fill holes:

* **Opening** → removes small blobs
* **Closing** → fills gaps inside the object

```python
cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
```

This step is crucial to ensure **clean contours** even when text or reflections are present on the object.

---

### 5.5 Contour Detection & Selection

Contours are extracted using:

```python
cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

To avoid tracking incorrect red objects, contours are filtered using:

* Area thresholds
* Compactness (circularity)
* Solidity and enclosure checks

The **best contour** is selected to represent the target object.

---

### 5.6 Centroid Estimation

The object position is computed using **image moments**:

```python
M = cv2.moments(contour)
cx = M["m10"] / M["m00"]
cy = M["m01"] / M["m00"]
```

This centroid is used as the **measurement input** for control and filtering.

---

## 6. State Estimation (Kalman Filter)

A **2D Kalman Filter** is used to:

* Smooth noisy centroid measurements
* Predict object motion
* Reduce jitter and oscillations

State vector:

```
[x, y, vx, vy]
```

Kalman filtering significantly improves tracking stability, especially when:

* The object moves quickly
* Temporary detection loss occurs

---

## 7. Control Strategy

### 7.1 Error Calculation

Tracking error is computed as:

```
error_x = object_x − frame_center_x
error_y = object_y − frame_center_y
```

Deadbands are applied to prevent micro-movements near the center.

---

### 7.2 Control Mapping

A **PD-like control law** converts pixel error into normalized servo commands:

* Proportional term → positional correction
* Derivative term → damping

Control outputs are clamped to **–1 to +1** to match Arduino constraints.

---

### 7.3 Command Throttling

To prevent servo saturation:

* Commands are rate-limited
* Serial messages are sent at fixed intervals

This ensures smooth, hardware-safe operation.

---

## 8. Multi-Colour Tracking

The system supports tracking of:

* Red
* Green
* Blue
* Yellow

Colour selection is controlled via keyboard input and dynamically switches HSV masks without restarting the system.

---

## 9. Face & Eye Colour Detection (Advanced Perception)

Using **Haar Cascade classifiers**:

* Face detection
* Eye detection 

Eye colour is estimated in HSV space and **temporally smoothed** to reduce flicker.

Importantly:

> Eye detection runs **in parallel** and does **not influence control decisions**.

This demonstrates **multi-task perception** in robotics.

---

## 10. Final Integrated System

The final script (`Auto_Tracking_final.py`) integrates:

* Vision
* Kalman filtering
* Control
* Serial communication
* Eye colour detection

Keyboard controls allow:

* Enabling/disabling tracking
* Switching colours
* Safe homing of the pan–tilt system

---

## 11. Limitations

* Performance depends on lighting conditions
* Haar cascades may struggle at long distances
* Designed for controlled indoor environments

---

## 12. Future Extensions

* YOLO-based object detection (comparison with HSV approach)
* Automatic PID tuning
* GUI-based parameter adjustment
* Depth-based tracking

---

## 13. Academic Relevance

This project demonstrates key concepts from:

* Computer Vision (OpenCV)
* Robot Sensing
* Signal Processing
* Feedback Control
* State Estimation
* System Integration

---

## 14. Author

**Iram Mukri**
M01092222

---


