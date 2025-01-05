import cv2
import threading
import time


class VideoCaptureDisplayThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.running = True
        self.iterations = 0

    def run(self):
        while self.running:
            ret, frame = self.cap.read()

            if frame is not None:
                cv2.imshow("Threaded Capture and Display", frame)

            self.iterations += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.running = False
                break

    def stop(self):
        self.running = False
        time.sleep(0.1)
        self.cap.release()
        cv2.destroyAllWindows()
