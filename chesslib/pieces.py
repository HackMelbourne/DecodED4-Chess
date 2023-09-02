class Piece:
    def __init__(self, color):
        self.color = color
        self.abbreviation = ""

    def __str__(self):
        return self.abbreviation
    
    def possible_moves(self):
        pass

    def place(self, board):
        pass


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "P"

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "N"

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "R"

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "B"

class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "Q"

class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.abbreviation = "K"


def generate_piece(letter):
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