from .utils import BoardCoordinates
from .constants import BOARD_SIZE

class InvalidPiece(Exception): pass

class Piece:
    def __init__(self, color):
        self.color = color
        self.abbreviation = ""

    def __str__(self):
        return self.abbreviation

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        pass

    def generic_moves(self, position: BoardCoordinates, orthogonal: bool, diagonal: bool, distance: int) -> list[BoardCoordinates]:
        orth = ((-1, 0), (0, -1), (0, 1), (1, 0))
        diag = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        legal_moves = []  # All legal positions the piece can move to
        directions = ()   # All possible directions the piece is allowed to move in

        if orthogonal and diagonal:
            directions = diag+orth
        elif diagonal:
            directions = diag
        elif orthogonal:
            directions = orth

        for x, y in directions:
            collision = False
            for step in range(1, distance + 1):
                # Check positions in the current (x, y) direction progressively, until the maximum distance
                if collision:
                    break

                destination = BoardCoordinates(position.row + step * y, position.col + step * x)
                if destination not in (self.board.occupied("white") + self.board.occupied("black")):
                    legal_moves.append(destination)
                elif not destination.is_in_bounds() or destination in self.board.occupied(self.color):
                    collision = True
                else:
                    # A piece cannot move past an opponent's piece, it must eat it first
                    legal_moves.append(destination)
                    collision = True

        # TODO: Check en passant
        return legal_moves

    def place(self, board):
        """ Keep a reference to the board """
        self.board = board


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "P"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        if self.color == "white":
            home_row = 1
            direction = 1
            enemy = "black"
        else:
            home_row = 6
            direction = -1
            enemy = "white"

        legal_moves = []
        blocked = self.board.occupied("white") + self.board.occupied("black")
        forward = BoardCoordinates(position.row + direction, position.col)

        # Can we move forward?
        if forward.is_in_bounds() and forward not in blocked:
            legal_moves.append(forward)
            if position.row == home_row:
                # If pawn in starting position we can do a double move
                double_forward = BoardCoordinates(forward.row + direction, forward.col)
                if double_forward.is_in_bounds() and double_forward not in blocked:
                    legal_moves.append(double_forward)

        # Attacking [-1, 1]
        for a in range(-1, 2, 2):
            attack = BoardCoordinates(position.row + direction, position.col + a)
            if attack.is_in_bounds() and attack in self.board.occupied(enemy):
                legal_moves.append(attack)

        return legal_moves


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "N"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        MOVES = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

        piece = self.board.get_piece_at(position)
        if piece is None:
            raise InvalidPiece

        legal_moves = []
        for x, y in MOVES:
            destination = BoardCoordinates(position.row + y, position.col + x)
            if destination.is_in_bounds() and destination not in self.board.occupied(piece.color):
                legal_moves.append(destination)

        return legal_moves


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "R"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().generic_moves(position, True, False, BOARD_SIZE)


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "B"

    def possible_moves(self, position: BoardCoordinates):
        return super().generic_moves(position, False, True, BOARD_SIZE)


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "Q"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().generic_moves(position, True, True, BOARD_SIZE)


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "K"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        # TODO: check castling
        return super().generic_moves(position, True, True, 1)


def generate_piece(letter: str) -> Piece | None:
    if letter in (None, " ") or len(letter) > 1:
        return

    if letter.isupper():
        color = "white"
    else:
        color = "black"

    piece = letter.upper()
    if piece == "P":
        return Pawn(color)
    if piece == "R":
        return Rook(color)
    if piece == "N":
        return Knight(color)
    if piece == "B":
        return Bishop(color)
    if piece == "Q":
        return Queen(color)
    if piece == "K":
        return King(color)
