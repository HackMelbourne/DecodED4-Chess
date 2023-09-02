# board.py
import re
from .utils import BoardCoordinates
from .pieces import generate_piece

# FEN notation for the initial board state
INIT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def expand_blanks(match):
    return " " * int(match.group(0))

class Board:
    def __init__(self):
        self.positions = [None]
        self.state = {}    # internal state of the board: dict[str, Piece]
        self.player_turn = "white"
        self.load(INIT_FEN)

    def load(self, config):
        """Import state from FEN notation"""
        fen = config.split(" ")
        fen[0] = re.compile(r"\d").sub(expand_blanks, fen[0])
        self.positions = [None]
        for x, row in enumerate(self._get_rows(fen[0])):
            for y, letter in enumerate(row):
                if self._is_cell_empty(letter):
                    continue
                coords = BoardCoordinates(7 - x, y)
                letter_coords = coords.letter_notation()
                self.state[letter_coords] = generate_piece(letter)
                self.state[letter_coords].place(self)

        if fen[1] == "w":
            self.player_turn = "white"
        else:
            self.player_turn = "black"

    def _get_rows(self, fen: str):
        return fen.split("/")

    def _is_cell_empty(self, val: str) -> bool:
        return val == " "
    
    def items(self):
        return self.state.items()
