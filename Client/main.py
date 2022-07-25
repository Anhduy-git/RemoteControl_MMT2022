try:
    import tkinter as tk
    from client import Client
    import constants
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pillow"]
    call("pip install " + ' '.join(modules), shell=True)

# Home page
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Client")
    canvas = tk.Canvas(root, width=constants.WIDTH, height=constants.HEIGHT)
    canvas.pack()

    Client(root).onCreate()

    root.mainloop()