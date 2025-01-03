import cv2
import threading
import time


class VideoDisplayThread(threading.Thread):
    def __init__(self, get_frame_function):
        super().__init__()
        self.get_frame = get_frame_function
        self.running = True
        self.iterations = 0

    def run(self):
        while self.running:
            frame = self.get_frame()

            if frame is not None:
                cv2.imshow("Threaded Display", frame)
                self.iterations += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.running = False
                break

    def stop(self):
        self.running = False
        time.sleep(0.1)
        cv2.destroyAllWindows()
