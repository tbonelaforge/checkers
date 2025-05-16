from typing import Union

from actions.jump_action import JumpAction
from actions.move_action import MoveAction

Action = Union[MoveAction, JumpAction]