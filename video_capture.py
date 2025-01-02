import cv2
import threading
import time
import queue


class VideoCaptureThread(threading.Thread):
    def __init__(self, frame_queue: queue.Queue):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame_queue = frame_queue
        self.running = True
        self.iterations = 0

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.frame_queue.put(frame)
            self.iterations += 1

    def stop(self):
        self.running = False
        time.sleep(0.3)
        self.cap.release()
