# OpenCV Threading Performance Test

This repository contains a Python project that tests the performance of video capture and display using OpenCV in various threading configurations. The test includes three scenarios:

1. **Single-threaded video capture and display** - Video capture and display in the same thread.
2. **Threaded video capture, display in main thread** - Video capture in a separate thread, display in the main thread.
3. **Fully threaded video capture and display** - Video capture and display in separate threads.

Each scenario includes a computationally intensive task running in the main thread to simulate load.

## Requirements

- Python 3.x
- OpenCV
- NumPy

## Usage

Run the script to test the performance of the different video capture scenarios:  
`python main.py`

Press 'q' to quit the test early.
