import tkinter as tk
from PIL import ImageTk, Image
from .board import Board
from .utils import letter_to_board_coords, BoardCoordinates

class BoardGui(tk.Frame):
    def __init__(self, parent, chessboard, squaresize=64):
        super().__init__()
        self.pieces = {}
        self.icons = {}
        self.rows = 8
        self.columns = 8
        self.square_size = squaresize
        self.chessboard = chessboard
        self.highlighted = None
        self.selected_piece = None

        canvas_width = self.columns * squaresize
        canvas_height = self.rows * squaresize

        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        self.color1 = "white"
        self.color2 = "grey"
        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.click)

    def click(self, event: tk.Event):
        print("mouse clicked")
        col_size = row_size = event.widget.master.square_size
        current_col = int(event.x / col_size)
        current_row = int(8 - (event.y / row_size))

        position = BoardCoordinates(current_row, current_col)

        if self.selected_piece is not None:
            print("second", self.selected_piece)
            # update position of piece
            self.move(self.selected_piece[1], position)
            self.selected_piece = None
            self.highlighted = None
            self.refresh(event)
            self.draw_pieces()

        # highlighting clicked square
        self.highlight(position)
        if self.highlighted is not None:
            for square in self.highlighted:
                self.square_background(square, "spring green")

    def move(self, p1, p2):
        piece = self.chessboard.get_piece_at(p1)
        dest_piece = self.chessboard.get_piece_at(p2)
        print(dest_piece)

        if dest_piece is not None and dest_piece.color == piece.color:
            return

        print(p1, p2)

        self.chessboard.move(p1, p2)

    def highlight(self, pos):
        piece = self.chessboard.get_piece_at(pos)
        print(piece)
        if piece is None or (piece.color != self.chessboard.player_turn):
            return

        self.selected_piece = (piece, pos)
        self.highlighted = [pos]
        print(self.selected_piece)

    def draw_pieces(self):
        self.canvas.delete("piece")   # clear all existing pieces on the canvas to prevent duplicates

        for coord, piece in self.chessboard.items():
            if piece is not None:
                coordinates = letter_to_board_coords(coord)
                self.draw_piece(piece, coordinates.row, coordinates.col)


    def draw_piece(self, piece, row, col):
        """Draw a piece on the board"""
        x = col * self.square_size
        y = (7-row) * self.square_size
        image_filename = f"img/{piece.color}{piece.abbreviation.lower()}.png"
        piece_name = f"{piece.abbreviation}{x}{y}"

        if image_filename not in self.icons:
            self.icons[image_filename] = ImageTk.PhotoImage(file=image_filename, width=32, height=32)

        self.add_piece(piece_name, self.icons[image_filename], row, col)

    def add_piece(self, name, image, row=0, col=0):
        """Place an image on the board"""
        x = (col + .5) * self.square_size
        y = (7 - (row - .5)) * self.square_size

        self.canvas.create_image(x, y, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, row, col)

    def place_piece(self, name, row, col):
        """Place a piece at the given row/column"""
        self.pieces[name] = (row, col)
        x = (col * self.square_size) + int(self.square_size / 2)
        y = ((7 - row) * self.square_size) + int(self.square_size / 2)
        self.canvas.coords(name, x, y)


    def square_background(self, coord, color=None):
        """Change the color of the square at `coord` to `color`"""
        if color is None:
            color = self.get_color_from_coords(coord)
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

    def refresh(self, e):
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


    def get_color_from_coords(self, coords: BoardCoordinates):
        return [self.color1, self.color2][(coords.row - coords.col) % 2]
        

def display(chessboard: Board):
    root: tk.Tk = tk.Tk()
    root.title("Python Chess")
    gui = BoardGui(root, chessboard)
    gui.pack(side="top", fill="both", expand=True, padx=4, pady=4)
    gui.draw_pieces()
    root.mainloop()