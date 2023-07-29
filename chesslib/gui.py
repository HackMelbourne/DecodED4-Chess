import tkinter as tk


class BoardGui(tk.Frame):
    def __init__(self, parent: tk.Tk, square_size=64):
        super().__init__()
        self.pieces = {}
        self.rows: int = 8
        self.columns: int = 8
        self.square_size: int = square_size

        canvas_width = self.columns * square_size
        canvas_height = self.rows * square_size

        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

    @property
    def canvas_size(self):
        return (self.columns * self.square_size,
                self.rows * self.square_size)


def display():
    root: tk.Tk = tk.Tk()
    root.title("Python Chess")

    gui = BoardGui(root)
    gui.pack(side="top", fill="both", expand=True, padx=4, pady=4)

    root.mainloop()


if __name__ == "__main__":
    display()
