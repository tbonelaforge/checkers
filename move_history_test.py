from sharedtypes.move_history import MoveHistory
from sharedtypes.game_step import GameStep
from actions.move_action import MoveAction
from checkers_board import BoardPositions


if __name__ == "__main__":
    print("ABout to construct a MoveHistory...")
    action1 = MoveAction(action_type="move", color='r', current_pos=[0, 0], final_pos=[0, 1])
    board_position1: BoardPositions = {
        '0,1': ['r', 'm']
    }
    
    action2 = MoveAction(action_type="move", color='b', current_pos=[1, 0], final_pos=[1, 0])
    board_position2: BoardPositions = {
        '1,0': ['b', 'k']
    }
    game_step1 = GameStep(move=action1, resulting_state=board_position1)
    game_step2 = GameStep(move=action2, resulting_state=board_position2)
    move_history = MoveHistory([game_step1, game_step2])
    print("Constructed move_history: ")
    print(move_history)
    print("The result of model_dump_json is: ")
    print(move_history.model_dump_json())
    print("After constructing a move history, how can I get the root? ")
    print("The dir of the move_history instance is: ")
    print(dir(move_history))
    print("The root is: ")
    print(move_history.root)