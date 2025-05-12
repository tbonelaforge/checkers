import numpy as np

from training import get_x_from_board_stats

class TargetFunction:
    def __init__(self, w=None):
        if w is None:
            w = np.array([
                -2.3259462,
                -31.64356388,
                29.2439482,
                -1.0,
                1.0,
                1.0,
                -1.0
            ])
        self.w = np.array(w)

    def __call__(self, x):
        '''
        Evaluate board for likelihood of computer (red player) winning
        x = [1, x1, x2, x3, x4, x5, x6],
        where:
        x1 = the number of black pieces on the board
        x2 = the number of red pieces on the board
        x3 = the number of black kings on the board
        x4 = the number of red kings on the board
        x5 = the number of black pieces threatened by red
        x6 = the number of red pieces threatened by black
        return 
        '''
        if not self.is_ambiguous(x):
            return self.deterministic_score(x)

        # otherwise, use the current value of the weights
        npx = np.array(x)
        return np.dot(self.w, npx)
    
    def deterministic_score(self, x):
        if self.is_ambiguous(x):
            return None
        (_, x1, x2, x3, x4, x5, x6) = x
        if x1 == 0 and x2 > 0: # Red already won! 
            return 100
        if x2 == 0 and x1 > 0: # Black already won :()
            return -100

    def is_ambiguous(self, x):
        (_, x1, x2, x3, x4, x5, x6) = x
        if x1 == 0 and x2 > 0: # Red already won! 
            return False
        if x2 == 0 and x1 > 0: # Black already won :()
            return False
        return True

    def update_w(self, new_w):
        self.w = new_w

    def get_w(self):
        return self.w
    

if __name__ == "__main__":
    print("About to make a TargetFunction instance: ")
    test_w = np.array([
        -2.3259462,
        -31.64356388,
        29.2439482,
        -1.0,
        1.0,
        1.0,
        -1.0
    ])
    tf = TargetFunction(test_w)
    print("Made target function: ")
    print(tf)
    print("Now trying to evaluate the target function on x: ")
    # b_stats = np.array([0, 3, 0, 0, 0, 0, 100])
    b_stats = np.array([2, 0, 0, 0, 0, 0, -100])
    x = get_x_from_board_stats(b_stats)
    y = tf(x)
    print("Got y: ")
    print(y)