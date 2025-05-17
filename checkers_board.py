from actions.jump_action import JumpAction
from actions.jump_action import JumpAction
from actions.move_action import MoveAction
from actions.move_action import MoveAction

from typing import Dict, Literal, List

# Example board positions: {'0,1': ['r', 'm'], '0,3': ['r', 'm'],}
BoardPosition = tuple[Literal['r', 'b'], Literal['m', 'k']]
BoardPositions = Dict[str, BoardPosition]

def get_opponent(current_player):
    if current_player == 'b':
        return 'r'
    else:
        return 'b'

def get_display_char(c, t):
    if c == 'r':
        if t == 'm':
            return 'r'
        else:
            return 'R'
    if c == 'b':
        if t == 'm':
            return 'b'
        else:
            return 'B'

def is_dark(i, j):
    return (i + j) % 2 == 1


def is_out_of_bounds(pos):
    (i, j) = pos
    if i < 0:
        return True
    if i >= 8:
        return True
    if j < 0:
        return True
    if j >= 8:
        return True
    return False


def get_jump_target(jumper_pos, jumpee_pos):
    vector = (
        jumpee_pos[0] - jumper_pos[0],
        jumpee_pos[1] - jumper_pos[1]
    )
    jump_target = (
        jumpee_pos[0] + vector[0],
        jumpee_pos[1] + vector[1]
    )
    return jump_target
    
class CheckersBoard:


    @staticmethod
    def from_board_positions(board_positions: BoardPositions):
        positions = dict()
        for (pos_key, piece) in board_positions.items():
            pos = tuple(map(int, pos_key.split(',')))
            positions[pos] = piece
        return CheckersBoard(positions)

    
    @staticmethod
    def generate_initial_positions():
        initial_positions = dict()
        for red_row in [0, 1, 2]:
            for j in range(8):
                if is_dark(red_row, j):
                    initial_positions[(red_row, j)] = ('r', 'm')
        for black_row in [5, 6, 7]:
            for j in range(8):
                if is_dark(black_row, j):
                    initial_positions[(black_row, j)] = ('b', 'm')
        return initial_positions
        
    def __init__(self, initial_positions=None):
        # initial_positions = {
        # (0, 1) : ('r', 'm'),
        # (0, 3) : ('r', 'm'),
        # ...
        # }
        self.board = [
            [None for j in range(8)]
            for i in range(8)
        ]
        if initial_positions is None:
            initial_positions = CheckersBoard.generate_initial_positions()
        for (pos, piece) in initial_positions.items():
            (i, j) = pos
            self.board[i][j] = piece

    def get_features(self) -> List[float]:
        x1 = 0.0 # black pieces
        x2 = 0.0 # red pieces
        x3 = 0.0 # black kings
        x4 = 0.0 # red kings
        x5 = 0.0 # black threatened
        x6 = 0.0 # red threatened
        for i in range(len(self.board)):
            row = self.board[i]
            for j in range(len(row)):
                cell = self.board[i][j]
                if cell is None:
                    continue
                (color, piece) = cell
                if color == 'b':
                    x1 += 1
                    if piece == 'k':
                        x3 += 1
                    if self.is_threatened((i, j)):
                        x5 += 1
                else: # color == 'r'
                    x2 += 1
                    if piece == 'k':
                        x4 += 1
                    if self.is_threatened((i, j)):
                        x6 += 1
        return [x1, x2, x3, x4, x5, x6] 

    def is_threatened(self, pos):
        (i, j) = pos
        (this_color, this_piece) = self.board[i][j]
        opponent_color = get_opponent(this_color)
        i_dir = -1 if this_color == 'b' else 1

        # Check opponent adjacent squares
        for j_dir in [-1, 1]:
            opponent_pos = (i + i_dir, j + j_dir)
            if not is_out_of_bounds(opponent_pos) and not self.is_empty(opponent_pos):
                if self.get_color(opponent_pos) == opponent_color:
                    jump_target = get_jump_target(opponent_pos, pos)
                    if not is_out_of_bounds(jump_target) and self.is_empty(jump_target):
                        return True
        
        # Check my adjacent squares
        i_dir *= -1
        for j_dir in [-1, 1]:
            adjacent_pos = (i + i_dir, j + j_dir)
            if not is_out_of_bounds(adjacent_pos) and not self.is_empty(adjacent_pos):
                if self.get_color(adjacent_pos) == opponent_color and self.get_piece_type(adjacent_pos) == 'k':
                    # return True
                    jump_target = get_jump_target(adjacent_pos, pos)
                    if not is_out_of_bounds(jump_target) and self.is_empty(jump_target):
                        return True
        return False

        

    def get_current_positions_json(self) -> BoardPositions:
        '''
        current_positions = {
        '0,1' : ('r', 'm'),
        '0,3' : ('r', 'k')
        }
        '''
        current_positions = dict()
        for i in range(len(self.board)):
            row = self.board[i]
            for j in range(len(row)):
                cell = row[j]
                if cell is None:
                    continue
                current_positions[f'{i},{j}'] = [cell[0], cell[1]]
        return current_positions


    def is_empty(self, pos):
        (i, j) = pos
        if self.board[i][j] is None:
            return True
        return False

    def is_valid_move(self, next_pos):
        if is_out_of_bounds(next_pos):
            return False
        return True if self.is_empty(next_pos) else False
    
    def is_valid_jump(self, pos1, pos2, pos3):
        if is_out_of_bounds(pos2) or is_out_of_bounds(pos3):
            return False
        if self.is_empty(pos2):
            return False
        if self.get_color(pos2) == self.get_color(pos1):
            return False
        if not self.is_empty(pos3):
            return False
        return True

    def get_color(self, pos):
        (i, j) = pos
        return self.board[i][j][0]

    def get_piece_type(self, pos):
        (i, j) = pos
        return self.board[i][j][1]

    def get_display_char(self, i, j):
        piece = self.board[i][j]
        (c, t) = piece
        return get_display_char(c, t)

    def get_i_dir(self, color):
        return -1 if color == 'b' else 1

    def get_diagonals(self, pos, i_dir):
        (i, j) = pos
        return [
            (i + i_dir, j - 1),
            (i + i_dir, j + 1)
        ]

    def set_king(self, pos):
        (i, j) = pos
        color = self.get_color(pos)
        self.board[i][j] = (color, 'k')
    
    def get_valid_next_moves(self, color):
        next_moves = []
        for i in range(8):
            for j in range(8):
                pos = (i, j)
                if self.is_empty(pos):
                    continue
                this_color = self.get_color(pos)
                if this_color != color:
                    continue
                i_dir = self.get_i_dir(color)
                for forward_pos in self.get_diagonals(pos, i_dir):
                    if self.is_valid_move(forward_pos):
                        next_moves.append(MoveAction(
                            color=color,
                            current_pos=pos,
                            final_pos=forward_pos
                        ))
                if self.get_piece_type(pos) == 'k':
                    for backward_pos in self.get_diagonals(pos, -1 * i_dir):
                        if self.is_valid_move(backward_pos):
                            next_moves.append(MoveAction(
                                color=color,
                                current_pos=pos,
                                final_pos=backward_pos
                            ))
        return next_moves
    
    def get_valid_next_actions(self, color, previous_action=None):
        if previous_action is not None and previous_action.color == color:
            pos = previous_action.final_pos
            return self.jumps_from_position(pos)
        valid_jumps = self.get_valid_next_jumps(color)
        if len(valid_jumps) > 0:
            return valid_jumps
        return self.get_valid_next_moves(color)
    
    def print_valid_next_actions_json(self, color, previous_action=None):
        actions = self.get_valid_next_actions(color, previous_action)
        to_print = [a.model_dump_json() for a in actions]
        return "[{}]".format(",".join(to_print))


    def get_valid_next_jumps(self, color):
        next_jumps = []
        for i in range(8):
            for j in range(8):
                pos = (i, j)
                if self.is_empty(pos):
                    continue
                if self.get_color(pos) != color:
                    continue
                next_jumps.extend(self.jumps_from_position(pos))
        return next_jumps
    
    def jumps_from_position(self, pos1):
        color = self.get_color(pos1)
        i_dir = self.get_i_dir(color)
        jumps = []
        (i, j) = pos1

        # try the natural direction
        pos2 = (i + i_dir, j - 1)
        pos3 = (i + 2 * i_dir, j - 2)
        if self.is_valid_jump(pos1, pos2, pos3):
            jumps.append(JumpAction(
                color=color,
                current_pos=pos1,
                jumped_pos=pos2,
                final_pos=pos3
            ))

        pos2 = (i + i_dir, j + 1)
        pos3 = (i + 2 * i_dir, j + 2)
        if self.is_valid_jump(pos1, pos2, pos3):
            jumps.append(JumpAction(
                color=color,
                current_pos=pos1,
                jumped_pos=pos2,
                final_pos=pos3
            ))
            
        if self.get_piece_type(pos1) == 'k': # try backwards
            pos2 = (i - i_dir, j - 1)
            pos3 = (i - 2 * i_dir, j - 2)
            if self.is_valid_jump(pos1, pos2, pos3):
                jumps.append(JumpAction(
                    color=color,
                    current_pos=pos1,
                    jumped_pos=pos2,
                    final_pos=pos3
                ))

            pos2 = (i - i_dir, j + 1)
            pos3 = (i - 2 * i_dir, j + 2)
            if self.is_valid_jump(pos1, pos2, pos3):
                jumps.append(JumpAction(
                    color=color,
                    current_pos=pos1,
                    jumped_pos=pos2,
                    final_pos=pos3
                ))
        return jumps

    def apply_action(self, action):
        assert self.is_empty(action.final_pos)
        (i, j) = action.current_pos
        (next_i, next_j) = action.final_pos
        if action.action_type == 'move':
            self.board[next_i][next_j] = self.board[i][j]
            self.board[i][j] = None
        elif action.action_type == 'jump':
            assert not self.is_empty(action.jumped_pos)
            assert self.get_color(action.jumped_pos) != self.get_color(action.current_pos)
            (jumped_i, jumped_j) = action.jumped_pos
            self.board[next_i][next_j] = self.board[i][j]
            self.board[jumped_i][jumped_j] = None
            self.board[i][j] = None
        else:
            raise Exception("Unrecognized action type...")
        if action.color == 'b' and next_i == 0 or action.color == 'r' and next_i == 7:
            self.set_king((next_i, next_j))
        
    
    def pretty_print(self):
        for i in range(8):
            print('{}|'.format(i), end='')
            for j in range(8):
                if self.is_empty((i, j)):
                    print(' ', end='')
                else:
                    piece = self.board[i][j]
                    (c, t) = piece
                    disp = get_display_char(c, t)
                    print('%s' % (disp), end='')
                print("|", end='')
                if j == 7:
                    print() # start next line
        print(' ', end='')
        for j in range(8):
            print(' {}'.format(j), end='')
        print()

    def html_print(self):
        html = '<table id="checkers-board">'
        def string_id(i, j):
            return "{}_{}".format(str(i), str(j))
        
        for i in range(8):
            html += '<tr>'
            for j in range(8):
                if is_dark(i, j):
                    html += '<td class="grey" i={} j={} id={}>'.format(i, j, string_id(i, j))
                else:
                    html += '<td i={} j={} id={}>'.format(i, j, string_id(i, j))
                if self.is_empty((i, j)):
                    html += ' '
                else:
                    display_char = self.get_display_char(i, j)
                    if display_char.lower() == 'r':
                        html += '<span class="red">{}</span>'.format(display_char)
                    else:
                        html += display_char
                html += '</td>'
            html += '</tr>'
        html += '</table>'
        return html



if __name__ == "__main__":
    print("Testing the CheckersBoard, with only three pieces on it:")
    test_positions = {
        (0,1) : ('r', 'm'),
        (0,3) : ('r', 'k'),
        (5,6) : ('b', 'm')
    }

    test_board = CheckersBoard(test_positions)
    test_board.pretty_print()
    print("Testing the CheckersBoard, with initial positions: ")
    initial_board = CheckersBoard()
    initial_board.pretty_print()

    print("Testing the CheckersBoard, for calculating jump positions...")
    test_positions2 = {
        (1, 4) : ('b', 'm'),
        (2, 5) : ('r', 'k'),
        (3, 6) : ('b', 'm'),
        (4, 1) : ('r', 'm'),
        (5, 2) : ('b', 'm'),
        (4, 3) : ('r', 'm'),
    }

    test_board2 = CheckersBoard(test_positions2)
    test_board2.pretty_print()

    print("Calculating jumps from pos 5,2")
    five_two_jumps = test_board2.jumps_from_position((5, 2))
    print("Got fvive_two_jumps: ")
    print(five_two_jumps)
    print("Calculating jumps from pos 2,5")
    two_five_jumps = test_board2.jumps_from_position((2, 5))
    print("Got two_five_jumps: ")
    print(two_five_jumps)

    print("Determing all regulare MOVES which are valid from test_board2...")
    all_red_moves = test_board2.get_valid_next_moves('r')
    print("Got all red_moves: ")
    print(all_red_moves)
    all_black_moves = test_board2.get_valid_next_moves('b')
    print("Got all black_moves: ")
    print(all_black_moves)
    print("Getting all black actions...")
    all_black_actions = test_board2.get_valid_next_actions('b')
    print(all_black_actions)

    print("Now applying a jump: curr: (5, 2) - jumped: (4, 3) - final: (3, 4)")
    jump_action = JumpAction('b', (5, 2), (4, 3), (3, 4))
    test_board2.apply_action(jump_action)
    print("After applying the jump action to test_board2, we have: ")
    test_board2.pretty_print()
    print("Given the previous move was a jump, the next actions are: ")
    all_black_actions2 = test_board2.get_valid_next_actions('b', previous_action=jump_action)
    print(all_black_actions2)
    
    print("For red, all available next_actions are: ")
    all_red_actions = test_board2.get_valid_next_actions('r')
    print(all_red_actions)

    print("Making an even simpler board: ")
    test_positions3 = {
        (1, 4) : ('b', 'm'),
        (2, 5) : ('r', 'k'),
        (3, 6) : ('b', 'm'),
        (4, 1) : ('r', 'm'),
        (4, 3) : ('r', 'm'),
    }

    test_board3 = CheckersBoard(test_positions3)
    test_board3.pretty_print()
    print("For black, all available next_actions are: ")
    all_black_actions = test_board3.get_valid_next_actions('b')
    print(all_black_actions)

    print("Testing the html_print function...")
    html = test_board3.html_print()
    print("Got html: ")
    print(html)

    print("All red actions (in json) are: ")
    actions_json = test_board3.print_valid_next_actions_json('r')
    print(actions_json)

    with open("templates/checkers_game_template.html") as f, open("test_html.html", 'w') as f_out:
        template = f.read()
        templated = template.replace('INSERT_TABLE_HERE', html)
        templated = templated.replace('INSERT_JSON_HERE', actions_json)
        f_out.write(templated)
        print("Just wrote the templated stuff...")
        

        
