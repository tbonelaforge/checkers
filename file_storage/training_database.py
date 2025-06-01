import csv
import numpy as np
import pandas as pd

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from file_storage.file_storage_utils import absolute_path, ensure_storage_directory, increment_counter, read_counter


DATA_EPOCHS_DIR = 'data-training'
COUNTER_FILENAME = 'howmany.txt'
EPOCHS_DIR = 'epochs'

ensure_storage_directory(DATA_EPOCHS_DIR, COUNTER_FILENAME, EPOCHS_DIR)

def get_filename_for_epoch_number(n):
    return absolute_path(f'{DATA_EPOCHS_DIR}/{EPOCHS_DIR}/epoch{n:05}.csv')

def record_epoch(training_data: np.ndarray):
    num_epochs = read_counter(DATA_EPOCHS_DIR, COUNTER_FILENAME)
    new_filename = get_filename_for_epoch_number(num_epochs + 1)
    with open(new_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(training_data)
    increment_counter(DATA_EPOCHS_DIR, COUNTER_FILENAME)

def read_last_epoch() -> np.ndarray:
    num_epochs = read_counter(DATA_EPOCHS_DIR, COUNTER_FILENAME)
    last_epochs_file = get_filename_for_epoch_number(num_epochs)
    epoch_dataframe = pd.read_csv(last_epochs_file, header=None)
    epoch_training_data = epoch_dataframe.to_numpy()
    return epoch_training_data
    
        