import cv2
import threading
import time


class VideoCaptureThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.running = True
        self.lock = threading.Lock()
        self.iterations = 0

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            with self.lock:
                self.frame = frame
            self.iterations += 1

    def stop(self):
        self.running = False
        time.sleep(0.1)
        self.cap.release()

    def get_frame(self):
        with self.lock:
            return self.frame
