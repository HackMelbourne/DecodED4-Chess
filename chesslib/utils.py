# utils.py

Y_AXIS_LABEL = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
X_AXIS_LABEL = tuple(range(1, 9))

class BoardCoordinates:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    # Convenient function that automatically converts the object to its string format when needed
    def __str__(self):
        return self.letter_notation().upper()

    def letter_notation(self) -> str | None:
        if not self.is_in_bounds():
            return
        return Y_AXIS_LABEL[int(self.col)] + str(X_AXIS_LABEL[int(self.row)])