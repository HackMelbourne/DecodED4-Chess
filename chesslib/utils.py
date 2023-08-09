from .constants import Y_AXIS_LABEL, X_AXIS_LABEL, BOARD_SIZE


class BoardCoordinates:
    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return self.letter_notation().upper()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def letter_notation(self) -> str | None:
        if not self.is_in_bounds():
            return
        return Y_AXIS_LABEL[int(self.y)] + str(X_AXIS_LABEL[int(self.x)])

    def number_notation(self) -> tuple[int, int]:
        return self.x, self.y

    def is_in_bounds(self):
        if self.y < 0 or self.y >= BOARD_SIZE or \
                self.x < 0 or self.x >= BOARD_SIZE:
            return False
        else:
            return True


def letter_to_board_coords(coord: str) -> BoardCoordinates:
    return BoardCoordinates(int(coord[1]) - 1, Y_AXIS_LABEL.index(coord[0]))