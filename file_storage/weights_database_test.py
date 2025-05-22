from weights_database import record_weights, read_last_weights
from shared.initial_w import initial_w

if __name__ == "__main__":
    print("About to record the following, initial weights array")
    record_weights(initial_w)
    print("Just recorded the initial_w, check the filesystem!")

    print("Reading the last weights in the database...")
    last_weights = read_last_weights()
    print("Got last_weights...")
    print(last_weights)