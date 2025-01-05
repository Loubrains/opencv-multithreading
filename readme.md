# OpenCV Threading Performance Test

This is a Python project that tests the performance of video capture and display using OpenCV in various threading configurations. The test includes three scenarios:

1. **Single-threaded video capture and display**
2. **Threaded video capture, display in main thread**
3. **Threaded video display, capture in main thread**
4. **Fully threaded video capture and display**
5. **Combined capture and display thread**

Each scenario includes a computationally intensive task running in the main thread to simulate load.

_The framerate is bottlednecked by both how quickly the program can capture, and how quickly it can display. Therefore, the unthreaded and partially threaded scenarios have basically the same frame rate, limited by the cpu intensive task. The fully threaded scenario and the combined capture+display thread scenario both have a high frame rate, unimpeded by the cpu intensive task._

## Requirements

- Python 3.x
- OpenCV
- NumPy

## Usage

Run the script to test the performance of the different video capture scenarios:  
`python main.py`

Press 'q' to quit each portion of the test.
