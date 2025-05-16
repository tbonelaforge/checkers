from pydantic import BaseModel
from typing import Literal, Union

class JumpAction(BaseModel):
    action_type: Literal['jump'] = 'jump'
    color: Literal['r', 'b']
    current_pos: tuple[int, int]
    final_pos: tuple[int, int]
    jumped_pos: tuple[int, int]


def __repr__(self):
    return "curr: {} - jumped: {} - final: {}".format(self.current_pos, self.jumped_pos, self.final_pos)