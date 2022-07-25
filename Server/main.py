import tkinter as tk
from server import Server
import constants

# Home page
if __name__ == "__main__":
    root = tk.Tk()

    canvas = tk.Canvas(root, width=constants.WIDTH, height=constants.HEIGHT)
    canvas.pack()

    Server(root).onCreate()

    root.mainloop()