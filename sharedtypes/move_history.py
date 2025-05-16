from typing import List
from pydantic import BaseModel, RootModel

from checkers_board import BoardPositions
from sharedtypes.action import Action
from sharedtypes.game_step import GameStep

class MoveHistory(RootModel):
    root: List[GameStep]