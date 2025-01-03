import cv2
import threading
import time
from video_capture import VideoCaptureThread


class VideoDisplayThread(threading.Thread):
    def __init__(self, video_thread: VideoCaptureThread):
        super().__init__()
        self.video_thread = video_thread
        self.running = True
        self.iterations = 0

    def run(self):
        while self.running:
            frame = self.video_thread.get_frame()
            if frame is not None:
                cv2.imshow("Threaded Capture and Display", frame)
                self.iterations += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.running = False
                break

    def stop(self):
        self.running = False
        time.sleep(0.1)
        cv2.destroyAllWindows()
