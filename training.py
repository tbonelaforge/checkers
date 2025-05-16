import numpy as np

def get_x_from_board_stats(b_stats):
    x = np.concatenate(([1], b_stats[:len(b_stats) - 1]))
    return x

def v_hat(w, x):
    return np.dot(w, x)

def train4(initial_w, initial_training_data):
    training_data = np.copy(initial_training_data)
    w = np.copy(1.0 * initial_w)
    num_passes = 50
    best_error = float("Infinity")
    best_w = None
    nu = 0.1
    
    for i in range(num_passes):
        this_error = get_total_squared_error(w, training_data)
        if this_error < best_error:
            best_error = this_error
            best_w = np.copy(w)

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


def train3(initial_w, initial_training_data):
    training_data = np.copy(initial_training_data)
    w = np.copy(1.0 * initial_w)
    num_passes = 50
    best_error = float("Infinity")
    best_w = None
    nu = 0.1
    
    for i in range(num_passes):
        this_error = get_total_squared_error(w, training_data)
        if this_error < best_error:
            best_error = this_error
            best_w = np.copy(w)
            
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
        




def process_training_examples2(w, training_examples):
    nu = 0.1
    for b_stats in training_examples:
        x = np.concatenate(([1], b_stats[:len(b_stats) - 1]))
        v_train_x = b_stats[len(b_stats) - 1]
        v_hat_x = v_hat(w, x)
        error_term = v_train_x - v_hat_x
        w_delta = np.array([0.0 for i in range(len(w))])
        for i in range(len(w)):
            w_delta[i] = nu * error_term *  x[i]
        w += w_delta
    return w


def process_training_examples(w, training_examples):
    # training_example = [1, 0, 0, 0, 0, 0, -100],
    # w = [0, -1, 1, -1, 1, 1, -1]
    nu = 0.1
    w_delta_total = [0.0 for i in range(len(w))]
    total_squared_error = 0.0
    for b_stats in training_examples:
        x = np.concatenate(([1], b_stats[:len(b_stats) - 1]))
        v_train_x = b_stats[len(b_stats) - 1]
        v_hat_x = v_hat(w, x)
        error_term = v_train_x - v_hat_x 
        total_squared_error += np.pow(error_term, 2)
        w_delta = np.array([0.0 for i in range(len(w))])
        for i in range(len(x)):
            w_delta[i] = nu * error_term * x[i]
        w_delta_total += w_delta
    return w_delta_total, total_squared_error

def get_total_squared_error(w, training_examples):
    total_squared_error = 0.0
    
    for b_stats in training_examples:
        x = np.concatenate(([1], b_stats[:len(b_stats) - 1]))
        v_train_x = b_stats[len(b_stats) - 1]
        v_hat_x = v_hat(w, x)
        error_term = v_train_x - v_hat_x 
        total_squared_error += np.pow(error_term, 2)
    return total_squared_error

if __name__ == "__main__":
    print("Starting with the following training data...")
    '''
    x0 = # constant 1
    x1 = # black pieces on board
    x2 = # red pieces on board
    x3 = # black kings on board
    x4 = # red kings on board
    x5 = # black pieces threatened
    x6 = # red pieces threatened
    '''
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

    '''
    V_hat(b) = w0 + w1 * x1 + w2 * x2 + w3 * x3 + w4 * x4 + w5 * x5 + w6 * x6
    '''
    print("now looping through the training examples")
    w = [0, -1, 1, -1, 1, 1, -1]
    # print("The w is: ")
    # print(w)

    # print("Initial total squared error is: ")
    # print(get_total_squared_error(w, initial_training_data))

    # w2 = process_training_examples2(w, initial_training_data)
    # print("The w2 is: ")
    # print(w2)
    # print("Now the error is: ")
    # print(get_total_squared_error(w2, initial_training_data))

    # w3 = process_training_examples2(w2, initial_training_data)
    # print("The w3 is: ")
    # print(w3)
    # print("Now the error is: ")
    # print(get_total_squared_error(w3, initial_training_data))
    num_passes = 50

    sanity_check_training_examples = np.array([
        [   2,    0,    0,    0,    0,    0, -100],
        [   0,    3,    0,    0,    0,    0,  100],
        [   3,    0,    0,    0,    0,    0, -100],
        [   0,    2,    0,    0,    0,    0,  100],
        [   0,    1,    0,    0,    0,    0,  100],
        [   0,    5,    0,    0,    0,    0,  100],
        [   0,    4,    0,    0,    0,    0,  100],
        [   5,    0,    0,    0,    0,    0, -100],
        [   1,    0,    0,    0,    0,    0, -100],
        [   4,    0,    0,    0,    0,    0, -100]
    ])
    baseline_training_data = np.copy(initial_training_data)
    np.random.shuffle(baseline_training_data)
    print("The shuffled data is: ")
    print(baseline_training_data)
    # baseline_training_data = np.copy(sanity_check_training_examples)
    print("Using baseline_training_data: ")
    print(baseline_training_data)
    for i in range(num_passes):
        print("w is: ")
        print(w)
        print("Squared Error is: ")
        print(get_total_squared_error(w, baseline_training_data))
        w_next = process_training_examples2(w, baseline_training_data)
        w = w_next

    

    print("Now using train3, get best w, best_error: ")
    w = np.array([0, -1, 1, -1, 1, 1, -1])
    (best_w, best_error) = train3(w, baseline_training_data)
    print("Got best_w, best_error: ")
    print(best_w)
    print(best_error)

    print("Now using train4, got best_w, best_error: ")
    w = np.array([0, -1, 1, -1, 1, 1, -1])
    (best_w, best_error) = train4(w, baseline_training_data)
    print("Got best_w, best_error: ")
    print(best_w)
    print(best_error)

    

    # print("The pathological ordering is: ")
    # pathological_ordering = np.array([
    #     [   0,    3,    0,    0,    0,    0,  100],
    #     [   2,    0,    0,    0,    0,    0, -100],
    #     [   4,    0,    0,    0,    0,    0, -100],
    #     [   1,    0,    0,    0,    0,    0, -100],
    #     [   0,    4,    0,    0,    0,    0,  100],
    #     [   3,    0,    0,    0,    0,    0, -100],
    #     [   0,    1,    0,    0,    0,    0,  100],
    #     [   0,    2,    0,    0,    0,    0,  100],
    #     [   5,    0,    0,    0,    0,    0, -100],
    #     [   0,    5,    0,    0,    0,    0,  100]
    # ])
    # print(pathological_ordering)
    # (check_w, check_e) = train3(w, pathological_ordering)
    # print("Got check_w, check_e: ")
    # print(check_w, check_e)


