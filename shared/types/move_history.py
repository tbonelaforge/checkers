from typing import List
from pydantic import BaseModel, RootModel

from checkers_board import BoardPositions
from shared.types.action import Action
from shared.types.game_step import GameStep

class MoveHistory(RootModel):
    root: List[GameStep]