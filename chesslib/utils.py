Y_AXIS_LABEL = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
X_AXIS_LABEL = tuple(range(1, 9))
BOARD_SIZE = 8

class BoardCoordinates:
    def __init__(self, x, y):
        self.row = int(x)
        self.col = int(y)

    def __str__(self):
        return self.letter_notation().upper()
    
    def letter_notation(self):
        if not self.is_in_bounds():
            return
        return str(Y_AXIS_LABEL[int(self.row)]) + str(X_AXIS_LABEL[int(self.col)])
    
    def is_in_bounds(self):
        if self.col < 0 or self.col >= BOARD_SIZE or \
                self.row < 0 or self.row >= BOARD_SIZE:
            return False
        else:
            return True
    

def letter_to_board_coords(coord):
    return BoardCoordinates(Y_AXIS_LABEL.index(coord[0]), int(coord[1])-1)



