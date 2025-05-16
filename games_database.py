import os

import json

from sharedtypes.move_history import MoveHistory
from sharedtypes.game_step import GameStep

from typing import Generator, List




DATA_DIR = 'data'
COUNTER_FILENAME = 'howmany.txt'
GAMES_DIR = 'games'
PADDING = 5 # Up to 10,000 games stored?

try:
    print(f'Ensuring data directory exists at {DATA_DIR}...')
    os.mkdir(DATA_DIR, 0o777)
    print(f'Created data directory at {DATA_DIR}')
    with open(f'{DATA_DIR}/{COUNTER_FILENAME}', 'w') as cf:
        print("Opened the counter file..")
        cf.write('0')
    os.mkdir(f'{DATA_DIR}/{GAMES_DIR}', 0o777)
    print(f'Created games directory at {DATA_DIR}/{GAMES_DIR}')
        
except FileExistsError as e:
    print(f'Data directory {DATA_DIR} already exists.')

def read_counter():
    with open(f'{DATA_DIR}/{COUNTER_FILENAME}', 'r') as cf:
        cf_text = cf.read()
        cf_num = int(cf_text) if len(cf_text) else 0
        return cf_num


def increment_counter():
    cf_num = read_counter()
    with open(f'{DATA_DIR}/{COUNTER_FILENAME}', 'w') as cf:
        cf.write(str(cf_num + 1))


def get_filename_for_game_number(n):
    return f'{DATA_DIR}/{GAMES_DIR}/game{n:05}.json'

def record_game(move_history: MoveHistory):
    num_games = read_counter()
    new_filename = get_filename_for_game_number(num_games + 1)
    with open(new_filename, 'w') as nf:
        nf.write(move_history.model_dump_json())
    increment_counter()

def read_all_games() -> Generator[List[GameStep]]:
    num_games = read_counter()
    for n in range(1, num_games + 1):
        game_file = get_filename_for_game_number(n)
        with open(game_file, 'r') as gf:
            game_steps_json = gf.read()
            game_steps = json.loads(game_steps_json)
            move_history = MoveHistory(game_steps)
            yield move_history.root


        
    
        

