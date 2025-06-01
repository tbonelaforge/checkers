import numpy as np
from checkers_board import CheckersBoard
import random

from typing import Callable, List, Literal

from estimate_training_data import get_training_vector
from shared import initial_w
from shared.types.action import Action
from target_function import TargetFunction



CheckersAI = Callable[[List[Action], Literal['b', 'r'], CheckersBoard], Action]


def get_other_player(current_player: Literal['b', 'r']) -> Literal['b', 'r']:
    return 'r' if current_player == 'b' else 'b'

def prompt_for_selection(actions):
    validated_selection = None
    while validated_selection is None:
        human_str = input("Which move do you choose? 0 - {}\n".format(len(actions) - 1))
        i = int(human_str)
        if i < 0 or i >= len(actions):
            print("Invalid selection")
            continue
        validated_selection = i
    print("You selected {}".format(repr(actions[i])))
    return validated_selection


def auto_play_game(black_ai: CheckersAI, red_ai: CheckersAI) -> Literal['b', 'r']:
    board = CheckersBoard()
    current_player = 'b'
    selected_action = None
    while True:
        board.pretty_print()
        valid_next_actions = board.get_valid_next_actions(current_player, selected_action)
        if len(valid_next_actions) == 0:
            winner = get_other_player(current_player)
            print("Player {} won the game!".format(winner))
            return winner
        if current_player == 'b':
            print(f'Player {current_player} turn')
            selected_action = black_ai(valid_next_actions, current_player, board)
            print(f'The AI for {current_player} selected move: {repr(selected_action)}')
        else: # current_player == 'r'
            print(f'Player {current_player} turn')
            selected_action = red_ai(valid_next_actions, current_player, board)
            print(f'The AI for {current_player} selected move: {repr(selected_action)}')
        board.apply_action(selected_action)
        if selected_action.action_type == 'jump':
            after_jump_actions = board.get_valid_next_actions(current_player, selected_action)
            if len(after_jump_actions):
                print("player {}'s turn again...".format(current_player))
                continue
        current_player = get_other_player(current_player)



def play_game():
    board = CheckersBoard()
    current_player = 'b'
    selected_action = None

    while True:
        board.pretty_print()
        valid_next_actions = board.get_valid_next_actions(current_player, previous_action=selected_action)
        if len(valid_next_actions) == 0:
            print("Player {} won the game!".format(get_other_player(current_player)))
            break
        if current_player == 'b':
            print("You are player 'b'")
            print("The valid next_actions are:")
            for i in range(len(valid_next_actions)):
                action = valid_next_actions[i]
                print("{}: {}".format(i, repr(action)))
            
            selection = prompt_for_selection(valid_next_actions)
            selected_action = valid_next_actions[selection]
        else:
            print("Computer turn")            
            selected_action = random.choice(valid_next_actions)
            print("Randomly selected move {}".format(repr(selected_action)))


        board.apply_action(selected_action)
        if selected_action.action_type == 'jump':
            after_jump_actions = board.get_valid_next_actions(current_player, selected_action)
            if len(after_jump_actions):
                print("player {}'s turn again...".format(current_player))
                continue
        current_player = get_other_player(current_player)




if __name__ == "__main__":
    play_game()
    
