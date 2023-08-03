import re

from .pieces import Piece, generate_piece
from .constants import *


def expand_blanks(match: re.Match[str]) -> str:
    return " " * int(match.group(0))


def number_notation(coord: str) -> tuple[int, int]:
    return int(coord[1])-1, Y_AXIS_LABEL.index(coord[0])


class BoardCoordinates:
    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def is_in_bounds(self):
        if self.y < 0 or self.y >= BOARD_SIZE or \
                self.x < 0 or self.x >= BOARD_SIZE:
            return False
        else:
            return True


class Board:
    """The chessboard class"""

    def __init__(self):
        self.positions = [None]
        self.state: dict[str, Piece] = {}
        self.player_turn = "white"
        self.load(INIT_FEN)

    def load(self, config: str):
        """Import state from FEN notation"""
        fen = config.split(" ")
        fen[0] = re.compile(r"\d").sub(expand_blanks, fen[0])
        self.positions = [None]
        for x, row in enumerate(self._get_rows(fen[0])):
            for y, letter in enumerate(row):
                if self._is_cell_empty(letter):
                    continue
                coords = BoardCoordinates(7 - x, y)
                letter_coords = self._coord_letter_notation(coords)
                self.state[letter_coords] = generate_piece(letter)
                self.state[letter_coords].place(self)

        if fen[1] == "w":
            self.player_turn = "white"
        else:
            self.player_turn = "black"

        # TODO: castling, en_passant, halfmove_clock, fullmove_clock

    def items(self):
        return self.state.items()

    def _coord_letter_notation(self, coord: BoardCoordinates) -> str | None:
        if not coord.is_in_bounds():
            return
        return Y_AXIS_LABEL[int(coord.y)] + str(X_AXIS_LABEL[int(coord.x)])

    def _get_rows(self, fen: str):
        return fen.split("/")

    def _is_cell_empty(self, val: str) -> bool:
        return val == " "

