import os

import json

import sys


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

print("After messing with the sys.path, it is now: ")
print(sys.path)

from shared.types.move_history import MoveHistory
from shared.types.game_step import GameStep

from typing import Generator, List

from file_storage.file_storage_utils import (
    ensure_storage_directory,
    read_counter,
    increment_counter,
    absolute_path,
)


DATA_DIR = "data-games"
COUNTER_FILENAME = "howmany.txt"
GAMES_DIR = "games"
PADDING = 5  # Up to 10,000 games stored?


ensure_storage_directory(DATA_DIR, COUNTER_FILENAME, GAMES_DIR)


def get_filename_for_game_number(n):
    return absolute_path(f"{DATA_DIR}/{GAMES_DIR}/game{n:05}.json")


def record_game(move_history: MoveHistory):
    num_games = read_counter(DATA_DIR, COUNTER_FILENAME)
    new_filename = get_filename_for_game_number(num_games + 1)
    with open(new_filename, "w") as nf:
        nf.write(move_history.model_dump_json())
    increment_counter(DATA_DIR, COUNTER_FILENAME)


def read_all_games() -> Generator[List[GameStep]]:
    num_games = read_counter(DATA_DIR, COUNTER_FILENAME)
    for n in range(1, num_games + 1):
        game_file = get_filename_for_game_number(n)
        with open(game_file, "r") as gf:
            game_steps_json = gf.read()
            game_steps = json.loads(game_steps_json)
            move_history = MoveHistory(game_steps)
            yield move_history.root
