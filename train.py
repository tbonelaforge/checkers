import numpy as np

def v_hat(w, x):
    return np.dot(w, x)

def get_total_squared_error(w, training_examples):
    total_squared_error = 0.0
    
    for b_stats in training_examples:
        x = np.concatenate(([1], b_stats[:len(b_stats) - 1]))
        v_train_x = b_stats[len(b_stats) - 1]
        v_hat_x = v_hat(w, x)
        error_term = v_train_x - v_hat_x 
        total_squared_error += np.pow(error_term, 2)
    return total_squared_error

def train(initial_w, initial_training_data):
    training_data = np.copy(initial_training_data)
    w = np.copy(1.0 * initial_w)
    num_passes = 50
    best_error = float("Infinity")
    best_w = None
    nu = 0.1
    
    for i in range(num_passes):
        # print("w is: ")
        # print(w)
        # print("Squared Error is: ")
        this_error = get_total_squared_error(w, training_data)
        # print(this_error)
        if this_error < best_error:
            best_error = this_error
            best_w = np.copy(w)
        else:
            # print("This error is not less than best_error...")
            pass
        
        # print(this_error)
        np.random.shuffle(training_data)
            
        for b_stats in training_data:
            x = np.concatenate(([1], b_stats[:len(b_stats) - 1]))
            v_train_x = b_stats[len(b_stats) - 1]
            v_hat_x = v_hat(w, x)
            error_term = v_train_x - v_hat_x
            w_delta = np.array([0.0 for i in range(len(w))])
            for i in range(len(w)):
                w_delta[i] = 1.0 * nu * error_term *  x[i]
            w += w_delta
        

    return (best_w, best_error)

if __name__ == "__main__":
    print("Using randomized ordering, with 50 passes, on initial data: ")
    initial_training_data = np.array([
        # <x1, x2, x3, x4, x5, x6, V_train>
        [1, 0, 0, 0, 0, 0, -100],
        [2, 0, 0, 0, 0, 0, -100],
        [3, 0, 0, 0, 0, 0, -100],
        [4, 0, 0, 0, 0, 0, -100],
        [5, 0, 0, 0, 0, 0, -100],
        [0, 1, 0, 0, 0, 0, 100],
        [0, 2, 0, 0, 0, 0, 100],
        [0, 3, 0, 0, 0, 0, 100],
        [0, 4, 0, 0, 0, 0, 100],
        [0, 5, 0, 0, 0, 0, 100]
    ])
    initial_w = np.array([0, -1, 1, -1, 1, 1, -1])
    (best_w, best_error) = train(initial_w, initial_training_data)
    print("Got best_w: ")
    print(best_w)
    print("Got best error: ")
    print(best_error)