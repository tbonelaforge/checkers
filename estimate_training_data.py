from typing import List
from games_database import read_all_games
from checkers_board import CheckersBoard
from sharedtypes.game_step import GameStep
from target_function import TargetFunction

from sharedtypes.move_history import MoveHistory


def get_training_vector(checkers_board):
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
    '''
    board_state = [
        [None, ['b', 'k'], None, ....],
        ...
    ]
    '''
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


def estimate_training_data(tf=None):
    raw_training_data = []
    
    if tf is None:
        tf = TargetFunction()
    move_history: MoveHistory
    for move_history in read_all_games():
        for i in range(len(move_history)):
            game_step: GameStep = move_history[i]
            checkers_board = get_checkers_board_at_game_step(game_step, should_print=True)
            x = get_training_vector(checkers_board)
            if tf.is_ambiguous(x):
                successor_game_step = find_successor_game_step(move_history, i)
                if successor_game_step is None:
                else:
                    next_checkers_board = get_checkers_board_at_game_step(successor_game_step, should_print=True)
                    print("Using the function on the successor gives x, v ")
                    next_x = get_training_vector(next_checkers_board)
                    print(next_x)
                    v = tf(next_x)
                    print(v)
            else:
                print("Using the actual value")
                print(tf(x))
            
            




if __name__ == "__main__":
    print("About to estimate training data: ")
    estimate_training_data()
