# gui.py
# https://www.alphr.com/install-pip-windows/
# py -m pip install Pillow

import tkinter as tk
from PIL import ImageTk, Image
from .board import Board
from .pieces import Piece

# gui.py

class BoardGui(tk.Frame):
    def __init__(self, parent, chessboard, square_size=64):
        super().__init__()
        self.pieces = {}
        self.icons  = {}    # To store the images for each piece
        self.rows = 8
        self.columns = 8
        self.square_size = square_size  # size of each square in the chess board

        canvas_width = self.columns * square_size
        canvas_height = self.rows * square_size

        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        # Added later
        self.color1 = "white"
        self.color2 = "grey"
        self.canvas.bind("<Configure>", self.refresh)

    def display(chessboard: Board):
        root: tk.Tk = tk.Tk()
        root.title("Python Chess")

        gui = BoardGui(root, chessboard)
        gui.pack(side="top", fill="both", expand=True, padx=4, pady=4)
        gui.draw_pieces()

        root.mainloop()

    def draw_pieces(self):
        self.canvas.delete("piece")   # clear all existing pieces on the canvas to prevent duplicates

        for coord, piece in self.chessboard.items():
            if piece is not None:
                coordinates = letter_to_board_coords(coords)
                self.draw_piece(piece, coordinates.row, coordinates.col)
    
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
        """Place an image on the board"""
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

    def square_background(self, coord: BoardCoordinates, color=None):
        """Change the color of the square at `coord` to `color`"""
        if color is None:
            color = get_color_from_coords(coord)
        x1 = (coord.col * self.square_size)
        y1 = ((7 - coord.row) * self.square_size)
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size

        # Draw a rectangle with the given colour
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")

        # see if we need to redraw a piece
        piece = self.chessboard.get_piece_at(coord)
        if piece is not None:
            self.draw_piece(piece, coord.row, coord.col)
    
    def refresh(self):
        """Redraw the board"""
        self.canvas.delete("square")
        
        # Alternating colours
        color = self.color2
        for row in range(self.rows):
            if color == self.color2:
                color = self.color1
            else:
                color = self.color2

            for col in range(self.columns):
                if self.highlighted is not None and BoardCoordinates(row, col) in self.highlighted:
                    self.square_background(BoardCoordinates(row, col), 'spring green')
                else:
                    self.square_background(BoardCoordinates(row, col), color)
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.place_piece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")