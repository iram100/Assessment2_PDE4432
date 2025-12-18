"""
multi_colour_tracker.py

Provides HSV masks for multiple selectable colours.
"""

import cv2
import numpy as np

HSV_PROFILES = {
    "red": [
        (np.array([0,120,60]),  np.array([10,255,255])),
        (np.array([170,120,60]),np.array([180,255,255]))
    ],
    "green": [
        (np.array([35,70,50]),  np.array([85,255,255]))
    ],
    "blue": [
        (np.array([90,80,50]),  np.array([130,255,255]))
    ],
    "yellow": [
        (np.array([20,100,100]),np.array([35,255,255]))
    ]
}

def build_colour_mask(hsv_img, colour_name):
    if colour_name not in HSV_PROFILES:
        return None

    mask = None
    for low, high in HSV_PROFILES[colour_name]:
        part = cv2.inRange(hsv_img, low, high)
        mask = part if mask is None else cv2.bitwise_or(mask, part)

    return mask
