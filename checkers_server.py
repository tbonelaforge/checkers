from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

from checkers_board import CheckersBoard, get_opponent, BoardPositions
from typing import List, Optional, Union, Dict
from pydantic import BaseModel

from actions.move_action import MoveAction
from actions.move_action import MoveAction
from actions.jump_action import JumpAction
from actions.jump_action import JumpAction

from games_database import record_game
import random

from sharedtypes.action import Action
from sharedtypes.move_history import GameStep, MoveHistory


class ComputerMoveBody(BaseModel):
    type: str




app = FastAPI()

checkers_board = CheckersBoard()
# test_positions3 = {
#         (1, 4) : ('b', 'm'),
#         (3, 6) : ('b', 'm'),
#     }

# checkers_board = CheckersBoard(test_positions3)
current_player = 'b'
# current_player = 'r'


previous_action = None





move_history : List[GameStep] = []


def print_winner_message(winner):
    return '<span id="winner-message"> %s WINS!</span>' % ('RED' if winner == 'r' else 'BLACK')

def record_action(player, action: Action, resulting_board: BoardPositions):
        move=action,
        resulting_state=resulting_board
    )
    move_history.append(
        game_step
    )

def handle_black_move(action: Action):
    global previous_action
    global current_player

    checkers_board.apply_action(action)
    record_action('b', action, checkers_board.get_current_positions_json())
    previous_action = action
    if action.action_type == 'jump':
        after_jump_actions = checkers_board.get_valid_next_actions('b', action)
        if len(after_jump_actions):
            return
    current_player = 'r'
    

def handle_red_move():
    global previous_action
    global current_player
    valid_next_actions = checkers_board.get_valid_next_actions('r', previous_action=previous_action)
    computer_action = random.choice(valid_next_actions)
    checkers_board.apply_action(computer_action)
    record_action('r', computer_action, checkers_board.get_current_positions_json())
    previous_action = computer_action
        
    if computer_action.action_type == 'jump':
        after_jump_actions = checkers_board.get_valid_next_actions('r', computer_action)
        if len(after_jump_actions):
            return
    current_player = 'b'


@app.get("/", response_class=HTMLResponse)
def template_html():
    
    html = checkers_board.html_print()
    actions_json = checkers_board.print_valid_next_actions_json(current_player, previous_action=previous_action)
    winner_message = ''
    if actions_json == '[]':
        winner_message = print_winner_message(get_opponent(current_player))
        record_game(MoveHistory(move_history))
    with open("templates/checkers_game_template.html") as t:
        template = t.read()
        templated = template.replace('INSERT_TABLE_HERE', html)
        templated = templated.replace('INSERT_JSON_HERE', actions_json)
        templated = templated.replace('INSERT_CURRENT_PLAYER_HERE', "'{}'".format(current_player))
        templated = templated.replace('INSERT_WINNER_MESSAGE_HERE', winner_message)
        return templated


@app.get("/static/{path}", response_class=FileResponse)
def static_file(path: str):
    return "./static/{}".format(path)

@app.post("/move")
def apply_move(body: Optional[Union[MoveAction, JumpAction, ComputerMoveBody]]):
    global previous_action
    if current_player == 'b':
        handle_black_move(body)        
    else: # current_player == 'r'    
        handle_red_move()
