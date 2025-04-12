import numpy as np

if __name__ == "__main__":
    print("Going to perform linear least squares...")
    A = np.array([
        [1, 1, 0],
        [1, 2, 0],
        [1, 3, 0],
        [1, 4, 0],
        [1, 5, 0],
        [1, 0, 1],
        [1, 0, 2],
        [1, 0, 3],
        [1, 0, 4],
        [1, 0, 5]
    ])

    b = np.array([
        -100,
        -100,
        -100,
        -100,
        -100,
        100,
        100,
        100,
        100,
        100
    ])
    w = np.linalg.lstsq(A, b)
    print("Got w: ")
    print(w)