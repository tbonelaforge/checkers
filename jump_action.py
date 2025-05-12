import json

class JumpAction:
    def __init__(self, color, pos1, pos2, pos3):
        self.action_type = 'jump'
        self.color = color
        self.current_pos = pos1
        self.final_pos = pos3
        self.jumped_pos = pos2


    def __repr__(self):
        return "curr: {} - jumped: {} - final: {}".format(self.current_pos, self.jumped_pos, self.final_pos)

    def model_dump(self):
        return {
            "type": "jump",
            "current": self.current_pos,
            "jumped": self.jumped_pos,
            "final": self.final_pos
        }

    def to_json(self):
        obj = self.model_dump()
        return json.dumps(obj)
