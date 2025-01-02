import cv2
import threading
import time
import numpy as np


# CPU-intensive operation
def cpu_expensive_task():
    # Generate two large random matrices
    matrix_a = np.random.rand(1000, 1000)
    matrix_b = np.random.rand(1000, 1000)

    # Perform matrix multiplication multiple times
    for _ in range(5):  # Adjust the number of iterations for higher intensity
        _ = np.dot(matrix_a, matrix_b)

    # Perform an FFT on a large array
    large_array = np.random.rand(1000000)
    _ = np.fft.fft(large_array)


# Scenario 1: Single-threaded video capture and display
def single_threaded_video(runtime):
    cap = cv2.VideoCapture(0)
    main_iterations = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Display the frame
        cv2.imshow("Single Thread", frame)

        # Perform the CPU-intensive task in the main thread
        cpu_expensive_task()
        main_iterations += 1

        if time.time() - start_time > runtime:  # Stop after n seconds
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Main thread iterations: {main_iterations}")


# Scenario 2: Separate thread for video capture
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


def threaded_video_capture(runtime):
    video_thread = VideoCaptureThread()
    video_thread.start()
    main_iterations = 0
    start_time = time.time()

    while True:
        frame = video_thread.get_frame()
        if frame is not None:
            cv2.imshow("Threaded Capture", frame)

        # Perform the CPU-intensive task in the main thread
        cpu_expensive_task()
        main_iterations += 1

        if time.time() - start_time > runtime:  # Stop after n seconds
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_thread.stop()
    video_thread.join()
    cv2.destroyAllWindows()

    print(f"Main thread iterations: {main_iterations}")
    print(f"Capture thread iterations: {video_thread.iterations}")


# Scenario 3: Separate threads for video capture and display
class VideoDisplayThread(threading.Thread):
    def __init__(self, video_thread):
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


def fully_threaded_video(runtime):
    video_thread = VideoCaptureThread()
    display_thread = VideoDisplayThread(video_thread)

    video_thread.start()
    display_thread.start()

    main_iterations = 0
    start_time = time.time()

    while display_thread.running:
        # Perform the CPU-intensive task in the main thread
        cpu_expensive_task()
        main_iterations += 1

        if time.time() - start_time > runtime:  # Stop after n seconds
            display_thread.running = False
            break

    video_thread.stop()
    display_thread.stop()
    video_thread.join()
    display_thread.join()

    print(f"Main thread iterations: {main_iterations}")
    print(f"Capture thread iterations: {video_thread.iterations}")
    print(f"Display thread iterations: {display_thread.iterations}")


if __name__ == "__main__":

    runtime = 10  # Number of seconds to run each scenario

    # print("Choose a scenario:")
    # print("1: Single-threaded video capture and display")
    # print("2: Threaded video capture, display in main thread")
    # print("3: Fully threaded video capture and display")
    # choice = input("Enter your choice (1/2/3): ").strip()

    # if choice == "1":
    #     single_threaded_video(runtime)
    # elif choice == "2":
    #     threaded_video_capture(runtime)
    # elif choice == "3":
    #     fully_threaded_video(runtime)
    # else:
    #     print("Invalid choice.")

    print("Scenario 1: Single-threaded video capture and display")
    single_threaded_video(runtime)
    print("\nScenario 2: Threaded video capture, display in main thread")
    threaded_video_capture(runtime)
    print("\nScenario 3: Fully threaded video capture and display")
    fully_threaded_video(runtime)
