import tkinter as tk

window = tk.Tk()

# Customising the window's title and size
window.title("Hello world")
window.geometry("300x300")

# Adding a Text Widget
hello = tk.Label(text="Hello world!")
hello.pack()

# Adding a Button Widget
button = tk.Button(text="Click me!")
button.pack()

tk.mainloop()