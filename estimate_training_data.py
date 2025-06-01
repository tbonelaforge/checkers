import json
import csv
from typing import List

import sys

print("Inside estimate_training_data, the sys.path is: ")
print(sys.path)

from file_storage.games_database import read_all_games
from checkers_board import CheckersBoard
from shared.types.game_step import GameStep
from target_function import TargetFunction

from shared.types.move_history import MoveHistory
import numpy as np

MAX_GAMES_TO_PROCESS = None


def dump_array_to_csv(data: np.ndarray, filename: str, delimiter=","):
    # data = [
    # [1.0, 12.0, 12.0, 0.0, 0.0, 0.0, 0.0, -30.12133436000002],
    # [1.0, 12.0, ...]
    # ...
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        writer.writerows(data)


def get_training_vector(checkers_board: CheckersBoard) -> List[float]:  #
    features = checkers_board.get_features()
    x = [1.0] + features
    return x


def get_checkers_board_at_game_step(game_step: GameStep, should_print=False):
    board_positions = game_step.resulting_state
    # board_positions = {
    #     '0,1' : ('r', 'm'),
    #     '0,3' : ('r', 'm'),
    #     ...
    # }

    checkers_board = CheckersBoard.from_board_positions(board_positions)
    if should_print:
        checkers_board.pretty_print()
    return checkers_board


def get_positions(board_state):
    """
    board_state = [
        [None, ['b', 'k'], None, ....],
        ...
    ]
    """
    positions = dict()
    for i in range(len(board_state)):
        row = board_state[i]
        for j in range(len(row)):
            cell = row[j]
            if cell is None:
                continue
            positions[(i, j)] = (cell[0], cell[1])
    return positions


def find_successor_game_step(move_history: List[GameStep], i):
    game_step: GameStep = move_history[i]
    current_player = game_step.move.color
    j = i + 1
    while j < len(move_history):
        next_step: GameStep = move_history[j]
        next_player = next_step.move.color
        if next_player == current_player:
            return next_step
        j += 1
    return None


def estimate_v(tf: TargetFunction, x: List[float], move_history: MoveHistory, i: int):
    if not tf.is_ambiguous(x):
        return tf(x)

    # tf.is_ambigous(x)
    successor_game_step = find_successor_game_step(move_history, i)
    if successor_game_step is None:
        v = tf(x)
        return v
    else:
        next_checkers_board = get_checkers_board_at_game_step(
            successor_game_step, should_print=True
        )
        next_x = get_training_vector(next_checkers_board)
        v = tf(next_x)
        return v


def estimate_training_data(tf=None) -> np.ndarray:
    training_data = []

    if tf is None:
        tf = TargetFunction()
    move_history: MoveHistory
    num_games_processed = 0
    for move_history in read_all_games():
        if MAX_GAMES_TO_PROCESS is not None:
            if num_games_processed >= MAX_GAMES_TO_PROCESS:
                break
        for i in range(len(move_history)):
            game_step: GameStep = move_history[i]
            checkers_board = get_checkers_board_at_game_step(
                game_step, should_print=False
            )
            x = get_training_vector(checkers_board)
            v: float = estimate_v(tf, x, move_history, i)
            training_row = x + [v]
            training_data.append(training_row)
        num_games_processed += 1
    return np.array(training_data)


if __name__ == "__main__":
    print("About to estimate training data: ")
    training_data: np.ndarray = estimate_training_data()
    print("Got training_data: ")
    print(training_data)
    print("The result of dumps on the training data is: ")
    print(json.dumps(training_data.tolist()))
    print("Going to write in csv format: ")
    epoch = 1
    csvfilename = f"./training_data/epoch{epoch}.csv"
    print(csvfilename)
    dump_array_to_csv(training_data, csvfilename)
    print("Check it now!")
