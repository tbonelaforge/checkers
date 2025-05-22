import os
import sys
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(SCRIPT_DIR)


from file_storage.file_storage_utils import absolute_path
from shared.initial_w import initial_w
from file_storage.training_database import read_last_epoch


MIN_PASSES = 50


def v_hat(w, x):
    return np.dot(w, x)


def get_error_term(w: np.ndarray, row: np.ndarray) -> tuple[float, np.ndarray]:
    x = row[:-1]
    v_train_y = row[len(row) - 1]
    v_hat_y = v_hat(w, x)
    error_term = v_train_y - v_hat_y
    return (error_term, x)


def get_total_squared_error(w: np.ndarray, training_examples: np.ndarray):
    total_squared_error = 0.0

    for row in training_examples:
        (error_term, x) = get_error_term(w, row)
        total_squared_error += np.pow(error_term, 2)
    return total_squared_error


def adjust_weights(
    initial_w: np.ndarray, initial_training_data: np.ndarray
) -> tuple[np.ndarray, float]:
    w = np.copy(1.0 * initial_w)
    training_data = np.copy(initial_training_data)
    original_error = get_total_squared_error(w, training_data)
    best_error = original_error
    best_w = np.copy(w)
    nu = 0.1

    for i in range(MIN_PASSES):
        np.random.shuffle(training_data)
        for row in training_data:
            (error_term, x) = get_error_term(w, row)
            w_delta = np.array([0.0 for i in range(len(w))])
            for i in range(len(w)):
                w_delta = 1.0 * nu * error_term * x[i]
            w += w_delta

        this_error = get_total_squared_error(w, training_data)
        if this_error < best_error:
            best_error = this_error
            best_w = np.copy(w)

    while best_error == original_error:
        np.random.shuffle(training_data)
        for row in training_data:
            (error_term, x) = get_error_term(w, row)
            w_delta = np.array([0.0 for i in range(len(w))])
            for i in range(len(w)):
                w_delta = 1.0 * nu * error_term * x[i]
            w += w_delta

        this_error = get_total_squared_error(w, training_data)
        if this_error < best_error:
            best_error = this_error
            best_w = np.copy(w)

    return (best_w, best_error)


def train_from_last_epoch(w: np.ndarray) -> tuple[np.ndarray, float]:
    training_data = read_last_epoch()
    original_error = get_total_squared_error(w, training_data)
    (new_w, new_error) = adjust_weights(w, training_data)
    print(new_w, new_error)
    return (new_w, new_error)


def train_from_file(w: np.ndarray, simple_csvfilename: str) -> tuple[np.ndarray, float]:
    csvfilename = absolute_path(simple_csvfilename)
    training_dataframe = pd.read_csv(csvfilename, header=None)
    training_data = training_dataframe.to_numpy()
    original_error = get_total_squared_error(w, training_data)
    (new_w, new_error) = adjust_weights(w, training_data)
    return (new_w, new_error)


if __name__ == "__main__":
    print("Testing the train_from_file methodology...")
    train_from_file(initial_w, "data-training/epochs/epoch00001.csv")

    print("Going to train from last epoch, starting from w = ")
    w = initial_w
    print(w)
    (new_w, new_error) = train_from_last_epoch(w)
    print("Got new_w, new_error")
    print(new_w)
    print(new_error)
