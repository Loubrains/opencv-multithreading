import cv2
import queue
import time
from video_capture import VideoCaptureThread
from video_display import VideoDisplayThread
from cpu_task import cpu_expensive_task


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
def threaded_video_capture(runtime):
    frame_queue = queue.Queue(maxsize=1)
    video_thread = VideoCaptureThread(frame_queue)
    video_thread.start()
    main_iterations = 0
    start_time = time.time()

    while True:
        try:
            frame = frame_queue.get_nowait()

            if frame is not None:
                cv2.imshow("Threaded Capture", frame)

            # Perform the CPU-intensive task in the main thread
            cpu_expensive_task()
            main_iterations += 1

        except queue.Empty:
            pass

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
def fully_threaded_video(runtime):
    frame_queue = queue.Queue(maxsize=1)
    video_thread = VideoCaptureThread(frame_queue)
    display_thread = VideoDisplayThread(frame_queue)

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
    runtime = 3  # Number of seconds to run each scenario

    print("Scenario 1: Single-threaded video capture and display")
    single_threaded_video(runtime)
    print("\nScenario 2: Threaded video capture, display in main thread")
    threaded_video_capture(runtime)
    print("\nScenario 3: Fully threaded video capture and display")
    fully_threaded_video(runtime)
