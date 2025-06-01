import math
import random
from typing import List, Literal
import numpy as np
from checkers_board import CheckersBoard
from checkers_game import auto_play_game
from estimate_training_data import get_training_vector
from shared.initial_w import initial_w
from shared.types.action import Action
from target_function import TargetFunction
from file_storage.weights_database import read_all_weights, read_weights_counter


def random_ai(
    valid_next_actions: List[Action],
    current_player: Literal["b", "r"],
    current_board: CheckersBoard,
) -> Action:
    choice = random.choice(valid_next_actions)
    return choice


def create_ml_ai_red(tf: TargetFunction):
    def ml_ai_red(
        valid_next_actions: List[Action],
        current_player: Literal["b", "r"],
        current_board: CheckersBoard,
    ):
        assert current_player == "r"
        # go for high scores
        # tf = TargetFunction()
        best_score = float("-Infinity")
        selected_action = None
        best_actions: List[Action] = []
        for valid_next_action in valid_next_actions:
            board_copy = CheckersBoard.from_board_positions(
                current_board.get_current_positions_json()
            )
            board_copy.apply_action(valid_next_action)
            next_x = get_training_vector(board_copy)
            score = tf(next_x)
            if score > best_score:
                best_actions = []
                best_score = score
                best_actions.append(valid_next_action)
            elif math.isclose(score, best_score):
                best_actions.append(valid_next_action)
        selected_action = random.choice(best_actions)
        return selected_action

    return ml_ai_red


def create_ml_ai_black(tf: TargetFunction):
    def ml_ai_black(
        valid_next_actions: List[Action],
        current_player: Literal["b", "r"],
        current_board: CheckersBoard,
    ):
        assert current_player == "b"
        # go for low scores
        # tf = TargetFunction()
        best_score = float("Infinity")
        selected_action = None
        best_actions: List[Action] = []
        for valid_next_action in valid_next_actions:
            board_copy = CheckersBoard.from_board_positions(
                current_board.get_current_positions_json()
            )
            board_copy.apply_action(valid_next_action)
            next_x = get_training_vector(board_copy)
            score = tf(next_x)
            if score < best_score:
                best_actions = []
                best_score = score
                best_actions.append(valid_next_action)
            elif math.isclose(score, best_score):
                best_actions.append(valid_next_action)
        selected_action = random.choice(best_actions)
        return selected_action

    return ml_ai_black


def accumulate_game_stats(black_player, red_player):
    game_winners = []
    for i in range(100):
        print(f"Auto-playing game {i}...")
        winner = auto_play_game(black_player, red_player)
        game_winners.append(winner)
    num_black_wins = game_winners.count("b")
    num_red_wins = game_winners.count("r")
    return (num_black_wins, num_red_wins)


def test_random_against_ml():
    ml_ai_red = create_ml_ai_red(TargetFunction(initial_w))

    (num_black_wins, num_red_wins) = accumulate_game_stats(random_ai, ml_ai_red)
    print(f"Red won {num_red_wins} times, Black won {num_black_wins} times")


def test_random_against_random():
    (num_black_wins, num_red_wins) = accumulate_game_stats(random_ai, random_ai)
    print(f"Red won {num_red_wins} times, Black won {num_black_wins} times")


def evaluate_ml() -> np.ndarray:
    n = read_weights_counter()
    matrix = np.zeros((n + 1, n + 1))  # first row and column is random player
    weights = list(read_all_weights())
    print("Got weights: ")
    print(weights)
    for i in range(n + 1):
        row_player = random_ai
        if i > 0:
            w_i = weights[i - 1]
            tf_i = TargetFunction(w_i)
            row_player = create_ml_ai_black(tf_i)
        for j in range(n + 1):
            col_player = random_ai
            if j > 0:
                w_j = weights[j - 1]
                tf_j = TargetFunction(w_j)
                col_player = create_ml_ai_red(tf_j)
            (num_black_wins, num_red_wins) = accumulate_game_stats(
                row_player, col_player
            )
            percentage = num_black_wins / (num_red_wins + num_black_wins)
            matrix[i][j] = percentage
    return matrix


if __name__ == "__main__":
    # print("Testing random against random...")
    # test_random_against_random()
    # print("Testing random against ml...")
    # test_random_against_ml()

    print("Testing all weights against all other weights")
    eval_matrix = evaluate_ml()
    print(eval_matrix)
