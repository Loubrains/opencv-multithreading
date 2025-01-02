import cv2
import threading
import time
import queue


class VideoDisplayThread(threading.Thread):
    def __init__(self, frame_queue: queue.Queue):
        super().__init__()
        self.frame_queue = frame_queue
        self.running = True
        self.iterations = 0

    def run(self):
        while self.running:
            try:
                frame = self.frame_queue.get_nowait()
                if frame is not None:
                    cv2.imshow("Threaded Capture and Display", frame)
                    self.iterations += 1
            except queue.Empty:
                pass

            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.running = False
                break

    def stop(self):
        self.running = False
        time.sleep(0.1)
        cv2.destroyAllWindows()
