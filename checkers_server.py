from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

from checkers_board import CheckersBoard, get_opponent
from typing import List, Optional, Union
from pydantic import BaseModel

from move_action import MoveAction
from jump_action import JumpAction

from games_database import record_game
import random


class MoveBody(BaseModel):
    type: str
    current: List[int]
    final: List[int]
    
class JumpBody(BaseModel):
    type: str
    current: List[int]
    final: List[int]
    jumped: List[int]

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

move_history = []



def print_winner_message(winner):
    return '<span id="winner-message"> %s WINS!</span>' % ('RED' if winner == 'r' else 'BLACK')

def hydrate_action(body: Union[MoveBody, JumpBody]):
    if body.type == 'move':
        action = MoveAction('b', body.current, body.final)
    elif body.type == 'jump':
        action = JumpAction('b', body.current, body.jumped, body.final)
    return action

def record_action(player, action, resulting_board):
    move_history.append(
        {
            'move':{'player': player, 'action': action.model_dump()},
            "resulting_state": resulting_board
        }
    )

def handle_black_move(body: Union[MoveBody, JumpBody]):
    global previous_action
    global current_player
    action = hydrate_action(body)
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
        record_game(move_history)
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
def apply_move(body: Optional[Union[MoveBody, JumpBody, ComputerMoveBody]]):
    global previous_action
    if current_player == 'b':
        handle_black_move(body)        
    else: # current_player == 'r'    
        handle_red_move()
