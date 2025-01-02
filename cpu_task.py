import numpy as np


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
