import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from estimate_training_data import estimate_training_data
from file_storage.training_database import record_epoch, read_last_epoch

if __name__ == "__main__":
    print("About to estimate training data, and write one epoch file")
    estimated_training_data = estimate_training_data()
    print(estimated_training_data)
    record_epoch(estimated_training_data)
    print("Now going to read_last_epoch:")
    written = read_last_epoch()
    print("Got written epoch: ")
    print(written)
