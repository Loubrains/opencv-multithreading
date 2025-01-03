import cv2
import threading
from collections import deque
import time


class VideoCaptureThread(threading.Thread):
    def __init__(self, frame_deque: deque):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame_deque = frame_deque
        self.running = True
        self.iterations = 0

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.frame_deque.append(frame)
            self.iterations += 1

    def stop(self):
        self.running = False
        time.sleep(0.1)
        self.cap.release()
