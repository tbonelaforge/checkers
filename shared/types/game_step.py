from pydantic import BaseModel

from checkers_board import BoardPositions
from shared.types.action import Action


class GameStep(BaseModel):
    move: Action
    resulting_state: BoardPositions

    