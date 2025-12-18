"""
kalman_tracker.py

2D Kalman filter for centroid prediction.
"""

import cv2
import numpy as np

class Kalman2D:
    def __init__(self):
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.transitionMatrix = np.array([
            [1,0,1,0],
            [0,1,0,1],
            [0,0,1,0],
            [0,0,0,1]
        ], np.float32)

        self.kf.measurementMatrix = np.array([
            [1,0,0,0],
            [0,1,0,0]
        ], np.float32)

        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.5

    def predict(self):
        pred = self.kf.predict()
        return int(pred[0]), int(pred[1])

    def correct(self, x, y):
        measurement = np.array([[np.float32(x)], [np.float32(y)]])
        self.kf.correct(measurement)
