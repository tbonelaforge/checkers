from pydantic import BaseModel
from typing import Literal

class MoveAction(BaseModel):
    action_type: Literal['move'] = 'move'
    color: Literal['r', 'b']
    current_pos: tuple[int, int]
    final_pos: tuple[int, int]

def __repr__(self):
        return "curr: {} - final: {}".format(self.current_pos, self.final_pos)

