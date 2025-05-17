import numpy as np
import pandas as pd

from shared.initial_w  import initial_w


NUM_PASSES = 50

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



def adjust_weights(initial_w: np.ndarray, initial_training_data: np.ndarray) -> tuple[np.ndarray, float]:
    w = np.copy(1.0 * initial_w)
    training_data = np.copy(initial_training_data)
    best_error = get_total_squared_error(w, training_data)
    best_w = np.copy(w)
    nu = 0.1

    for i in range(NUM_PASSES):
        # print("performing pass: %d" % (i))
        
        np.random.shuffle(training_data)
        for row in training_data:
            # x = row[:-1]
            # v_train_y = row[len(row) - 1]
            # v_hat_y = v_hat(w, x)
            # error_term = v_train_y - v_hat_y
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

def train_from_file(w: np.ndarray, csvfilename: str) -> tuple[np.ndarray, float]:
    training_dataframe = pd.read_csv(csvfilename, header=None)
    print("Got training_data (as pandas dataframe): ")
    print(training_dataframe)
    print("Converting the dataframe to a numpy array...")
    training_data = training_dataframe.to_numpy()
    print(training_data)
    print("Before adjusting the weights, we have w, total error:  ")
    original_error = get_total_squared_error(w, training_data)
    print(w, original_error)
    print("After adjusting the weights we have: ")
    (new_w, new_error) = adjust_weights(w, training_data)
    print(new_w, new_error)

if __name__ == "__main__":
    print("Testing the train_from_file methodology...")
    train_from_file(initial_w, './training_data/epoch1.csv')