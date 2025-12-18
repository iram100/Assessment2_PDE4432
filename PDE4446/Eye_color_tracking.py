"""
eye_colour_detection_stable.py

Stabilised face → eye → eye-colour detection.
- Restricted ROI (upper face only)
- Temporal smoothing to reduce flicker
- Parallel perception (no control interference)
"""

import cv2
import numpy as np
from collections import deque

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
EYE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# temporal buffer for eye colour
EYE_HISTORY = deque(maxlen=10)


def classify_eye_colour(hsv_eye):
    if hsv_eye.size == 0:
        return None

    h = np.mean(hsv_eye[:,:,0])
    s = np.mean(hsv_eye[:,:,1])
    v = np.mean(hsv_eye[:,:,2])

    if v < 40:
        return "dark"
    if h < 20:
        return "brown"
    if 20 <= h < 35:
        return "hazel"
    if 35 <= h < 85:
        return "green"
    if 85 <= h < 130:
        return "blue"
    return "unknown"


def detect_eyes_and_colour(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

    detected_colour = None

    for (x,y,w,h) in faces[:1]:
        # draw face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        # only upper half of face
        roi_gray = gray[y:y+h//2, x:x+w]
        roi_hsv  = hsv[y:y+h//2, x:x+w]

        eyes = EYE_CASCADE.detectMultiScale(roi_gray, 1.2, 5)

        for (ex,ey,ew,eh) in eyes[:2]:
            eye_hsv = roi_hsv[ey:ey+eh, ex:ex+ew]
            colour = classify_eye_colour(eye_hsv)

            if colour:
                EYE_HISTORY.append(colour)

            cv2.rectangle(frame,
                (x+ex, y+ey),
                (x+ex+ew, y+ey+eh),
                (0,255,0), 2)

        break

    if len(EYE_HISTORY) > 0:
        detected_colour = max(set(EYE_HISTORY), key=EYE_HISTORY.count)

    return detected_colour, frame
