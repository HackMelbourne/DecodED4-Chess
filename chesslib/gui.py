import tkinter as tk
from PIL import ImageTk, Image

from .board import Board, number_notation
from .pieces import Piece


class BoardGui(tk.Frame):
    def __init__(self, parent: tk.Tk, chessboard: Board, square_size=64):
        super().__init__()
        self.pieces: dict[str, tuple[int, int]] = {}   # { piece_name: (x, y) }; piece_name = {piece.abbreviation}{x}{y}
        self.icons: dict[str, ImageTk.PhotoImage] = {}
        self.rows: int = 8
        self.columns: int = 8
        self.chessboard: Board = chessboard
        self.square_size: int = square_size

        canvas_width = self.columns * square_size
        canvas_height = self.rows * square_size

        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

    def draw_pieces(self):
        self.canvas.delete("piece")

        for coord, piece in self.chessboard.items():
            if piece is not None:
                x, y = number_notation(coord)
                self.draw_piece(piece, x, y)

    def draw_piece(self, piece: Piece, row: int, col: int):
        """Draw a piece on the board"""
        x = col * self.square_size
        y = (7-row) * self.square_size
        image_filename = f"img/{piece.color}{piece.abbreviation.lower()}.png"
        piece_name = f"{piece.abbreviation}{x}{y}"

        if image_filename not in self.icons:
            self.icons[image_filename] = ImageTk.PhotoImage(file=image_filename, width=32, height=32)

        self.add_piece(piece_name, self.icons[image_filename], row, col)

    def add_piece(self, name: str, image: ImageTk.PhotoImage, row=0, col=0):
        x = (col + .5) * self.square_size
        y = (7 - (row - .5)) * self.square_size

        self.canvas.create_image(x, y, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, row, col)

    def place_piece(self, name: str, row: int, col: int):
        """Place a piece at the given row/column"""
        self.pieces[name] = (row, col)
        x = (col * self.square_size) + int(self.square_size / 2)
        y = ((7 - row) * self.square_size) + int(self.square_size / 2)
        self.canvas.coords(name, x, y)

    @property
    def canvas_size(self):
        return (self.columns * self.square_size,
                self.rows * self.square_size)


def display(chessboard: Board):
    root: tk.Tk = tk.Tk()
    root.title("Python Chess")

    gui = BoardGui(root, chessboard)
    gui.pack(side="top", fill="both", expand=True, padx=4, pady=4)
    gui.draw_pieces()

    root.mainloop()


if __name__ == "__main__":
    display()
