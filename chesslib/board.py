import re
from .utils import BoardCoordinates
from .pieces import generate_piece

# FEN notation for the initial board state
INIT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class ChessError(Exception): pass
class InvalidCoord(ChessError): pass
class InvalidColor(ChessError): pass
class InvalidMove(ChessError): pass
class Check(ChessError): pass
class CheckMate(ChessError): pass
class Draw(ChessError): pass
class NotYourTurn(ChessError): pass

def expand_blanks(match):
    return " " * int(match.group(0))

class Board:
    def __init__(self):
        self.positions = [None]
        self.state = {}    # internal state of the board: dict[str, Piece]
        self.player_turn = "white"
        self.load(INIT_FEN)

    def move(self, p1, p2):
        moved_piece = self.get_piece_at(p1)
        dest_piece = self.get_piece_at(p2)

        if self.player_turn != moved_piece.color:
            print(moved_piece.color)
            raise NotYourTurn("Not your turn")

        self._do_move(p1, p2)
        self._finish_move(moved_piece, dest_piece, p1, p2)

    def _do_move(self, p1, p2):
        moved_piece = self.get_piece_at(p1)
        self._update_coord_piece(p1, None)
        self._update_coord_piece(p2, moved_piece)

    def _update_coord_piece(self, coord, piece):
        pos = str(coord)
        if piece is None:
            del self.state[pos]
        else:
            self.state[pos] = piece

    def _finish_move(self, moved_piece, dest_piece, p1, p2):
        enemy = self.get_opponent(moved_piece.color)
        self.player_turn = enemy
        print(self.player_turn)
        abbr = moved_piece.abbreviation

        # print out moves
        if dest_piece is None:
            movetext = abbr + p2.letter_notation().lower()
        else:
            movetext = abbr + "x" + p2.letter_notation()

        print("Move: " + movetext)

    def get_opponent(self, color):
        if color == "white":
            return "black"
        return "white"

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
                print(letter, row)
                self.state[letter_coords] = generate_piece(letter)
                self.state[letter_coords].place(self)

        if fen[1] == "w":
            self.player_turn = "white"
        else:
            self.player_turn = "black"

    def _get_rows(self, fen):
        return fen.split("/")
    
    def _is_cell_empty(self, val):
        return val == " "
    
    def items(self):
        return self.state.items()
    
    def get_piece_at(self, coord):
        pos = str(coord)
        if pos not in self.state:
            return None
        return self.state[pos]
