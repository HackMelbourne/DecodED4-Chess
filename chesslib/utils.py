from .constants import Y_AXIS_LABEL, X_AXIS_LABEL, BOARD_SIZE


class BoardCoordinates:
    def __init__(self, row: int, col: int):
        self.row = int(row)
        self.col = int(col)

    def __str__(self):
        return self.letter_notation().upper()

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def letter_notation(self) -> str | None:
        if not self.is_in_bounds():
            return
        return Y_AXIS_LABEL[int(self.col)] + str(X_AXIS_LABEL[int(self.row)])

    def number_notation(self) -> tuple[int, int]:
        return self.row, self.col

    def is_in_bounds(self):
        if self.col < 0 or self.col >= BOARD_SIZE or \
                self.row < 0 or self.row >= BOARD_SIZE:
            return False
        else:
            return True


def letter_to_board_coords(coord: str) -> BoardCoordinates:
    return BoardCoordinates(int(coord[1]) - 1, Y_AXIS_LABEL.index(coord[0]))