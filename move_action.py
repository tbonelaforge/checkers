class MoveAction:
    def __init__(self, color, pos, next_pos):
        self.action_type = 'move'
        self.color = color
        self.current_pos = pos
        self.final_pos = next_pos

    def __repr__(self):
        return "curr: {} - final: {}".format(self.current_pos, self.final_pos)
