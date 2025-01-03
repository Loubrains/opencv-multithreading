import cv2
import threading
import time


class VideoCaptureThread(threading.Thread):
    def __init__(self, lock: threading.Lock):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.running = True
        self.lock = lock
        self.iterations = 0

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.lock.acquire(blocking=False):
                self.frame = frame
                self.iterations += 1
                self.lock.release()

    def stop(self):
        self.running = False
        time.sleep(0.1)
        self.cap.release()

    def get_frame(self):
        if self.lock.acquire(blocking=False):
            frame = self.frame
            self.lock.release()
            return frame
        return None
