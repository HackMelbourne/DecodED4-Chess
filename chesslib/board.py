import re
from copy import deepcopy

from .pieces import Piece, generate_piece, King, Rook, Pawn
from .constants import *
from .utils import BoardCoordinates, letter_to_board_coords


class ChessError(Exception): pass
class InvalidCoord(ChessError): pass
class InvalidColor(ChessError): pass
class InvalidMove(ChessError): pass
class Check(ChessError): pass
class CheckMate(ChessError): pass
class Draw(ChessError): pass
class NotYourTurn(ChessError): pass


def expand_blanks(match: re.Match[str]) -> str:
    return " " * int(match.group(0))


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
                letter_coords = coords.letter_notation()
                self.state[letter_coords] = generate_piece(letter)
                self.state[letter_coords].place(self)

        if fen[1] == "w":
            self.player_turn = "white"
        else:
            self.player_turn = "black"

        # TODO: castling, en_passant, halfmove_clock, fullmove_clock

    def move(self, p1: BoardCoordinates, p2: BoardCoordinates):
        """Makes a move from position p1 to p2"""
        moved_piece = self.get_piece_at(p1)
        dest_piece = self.get_piece_at(p2)

        if self.player_turn != moved_piece.color:
            raise NotYourTurn("Not " + moved_piece.color + "'s turn")

        enemy = self.get_opponent(moved_piece.color)
        possible_moves = moved_piece.possible_moves(p1)

        if p2 not in possible_moves:
            raise InvalidMove

        # If enemy has any moves look for check
        if self._all_possible_moves(enemy) and self.is_in_check_after_move(p1, p2):
            raise Check
        if not possible_moves and self.is_in_check(moved_piece.color):
            raise CheckMate
        elif not possible_moves:
            raise Draw

        self._do_move(p1, p2)
        self._finish_move(moved_piece, dest_piece, p1, p2)

    def _do_move(self, p1: BoardCoordinates, p2: BoardCoordinates):
        """Move a piece without validation"""
        moved_piece = self.get_piece_at(p1)
        self._update_coord_piece(p1, None)
        self._update_coord_piece(p2, moved_piece)

    def _finish_move(self, player: Piece, dest: Piece, p1: BoardCoordinates, p2: BoardCoordinates):
        """Set next player's turn, count moves, log moves, etc."""
        enemy = self.get_opponent(player.color)
        self.player_turn = enemy
        abbr = player.abbreviation

        if dest is None:
            movetext = abbr + p2.letter_notation().lower()
        else:
            movetext = abbr + "x" + p2.letter_notation()

        print("move: " + movetext)


    def items(self):
        return self.state.items()

    def get_piece_at(self, coord: BoardCoordinates) -> Piece | None:
        """Find the piece in board with coordinates `coord`"""
        pos = str(coord)
        if pos not in self.state:
            return None
        return self.state[pos]

    def _update_coord_piece(self, coord: BoardCoordinates, piece: Piece | None):
        """
        Update board state with the piece and coordinate.
        If piece is `None`, the coordinate is unoccupied
        """
        pos = str(coord)
        if piece is None:
            del self.state[pos]
        else:
            self.state[pos] = piece

    def occupied(self, color: str) -> list[BoardCoordinates]:
        """
            Return a list of coordinates occupied by `color`
        """
        result = []
        if color not in ("black", "white"):
            raise InvalidColor

        for coord in self.state:
            if self.state[coord].color == color:
                result.append(coord)

        return list(map(letter_to_board_coords, result))

    def is_in_check_after_move(self, p1: BoardCoordinates, p2: BoardCoordinates) -> bool:
        tmp = deepcopy(self)
        tmp._do_move(p1, p2)
        return tmp.is_in_check(self.get_piece_at(p1).color)

    def is_in_check(self, color: str) -> bool:
        self._verify_color(color)
        king_location = self._get_king_position(color)
        opponent = self.get_opponent(color)
        return king_location in self._all_possible_moves(opponent)

    def get_opponent(self, color: str):
        if color == "white":
            return "black"
        return "white"

    def _get_king(self ,color: str) -> Piece:
        self._verify_color(color)
        return self.state[self._get_king_position(color).letter_notation()]

    def _get_king_position(self, color: str) -> BoardCoordinates:
        for pos in list(self.state.keys()):
            if self.is_king(self.state[pos]) and self.state[pos].color == color:
                return letter_to_board_coords(pos)

    def _has_possible_moves(self, color: str) -> bool:
        return len(self._all_possible_moves(color)) > 0

    def _all_possible_moves(self, color: str) -> list[BoardCoordinates]:
        """Returns a list of `color`'s possible moves. Does not check for check."""
        if color not in ("black", "white"):
            raise InvalidColor

        result = []
        for coord in list(self.state.keys()):
            if (self.state[coord] is not None) and self.state[coord].color == color:
                moves = self.state[coord].possible_moves(letter_to_board_coords(coord))
                if moves:
                    result += moves
        return result

    def _check_repeated_moves(self):
        """Game draws after both players play the same move for 3 times"""
        if self.positions[-1] in self.positions[:-1]:
            count = 1
            for position in self.positions[:-1]:
                count += (position == self.positions[-1])
            print(f"repitition count: {count}")
            if count >= 3:
                raise Draw

    def _verify_color(self, color: str):
        if color not in ("black", "white"):
            raise InvalidColor

    def _get_rows(self, fen: str):
        return fen.split("/")

    def _is_cell_empty(self, val: str) -> bool:
        return val == " "

    def is_king(self, piece):
        return isinstance(piece, King)

    def is_rook(self, piece):
        return isinstance(piece, Rook)

    def is_pawn(self, piece):
        return isinstance(piece, Pawn)

