
from typing import Generator
import numpy as np

import os
import sys

import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from file_storage.file_storage_utils import absolute_path, ensure_storage_directory, read_counter, increment_counter





DATA_WEIGHTS_DIR = 'data-weights'
COUNTER_FILENAME='howmany.txt'
WEIGHTS_DIR='weights'

ensure_storage_directory(DATA_WEIGHTS_DIR, COUNTER_FILENAME, WEIGHTS_DIR)

def get_filename_for_weights_number(n):
    return absolute_path(f'{DATA_WEIGHTS_DIR}/{WEIGHTS_DIR}/weights{n:05}.json')

def read_weights_counter() -> int:
    return read_counter(DATA_WEIGHTS_DIR, COUNTER_FILENAME)

def record_weights(weights: np.ndarray):
    num_weights = read_counter(DATA_WEIGHTS_DIR, COUNTER_FILENAME)
    new_filename = get_filename_for_weights_number(num_weights + 1)
    with open(new_filename, 'w') as nf:
        nf.write(json.dumps(weights.tolist()))
    increment_counter(DATA_WEIGHTS_DIR, COUNTER_FILENAME)

def read_last_weights() -> np.ndarray:
    num_weights = read_counter(DATA_WEIGHTS_DIR, COUNTER_FILENAME)
    last_weights_file = get_filename_for_weights_number(num_weights)
    with open(last_weights_file, 'r') as wf:
        weights_json = wf.read()
        weights = np.array(json.loads(weights_json))
        return weights
    
def read_all_weights() -> Generator[np.ndarray]:
    num_games = read_counter(DATA_WEIGHTS_DIR, COUNTER_FILENAME)
    for n in range(1, num_games + 1):
        weights_file = get_filename_for_weights_number(n)
        with open(weights_file, 'r') as wf:
            weights_json = wf.read()
            plain_weights = json.loads(weights_json)
            yield np.array(plain_weights)