import tkinter as tk
from threading import Thread
import constants
import serverFeatures


class Server:
    def __init__(self, root):
        self.root = root
        self.button = None

    def onServerStartButtonPressed(self):
        serverFeatures.setUpServer()


    def onCreate(self):
        # init frame
        self.frame = tk.Frame(self.root, bg=constants.bgColor)
        self.frame.place(relwidth=1, relheight=1)

        # button click menu
        txtStartServer = tk.StringVar()
        self.startServerBtn = tk.Button(self.frame, textvariable=txtStartServer, font=constants.mainFont, bg="#20bebe",
                                        fg="white")
        self.startServerBtn.place(x=50, y=50, relwidth=1, relheight=1, width=-100, height=-100)
        self.startServerBtn.config(command=lambda: self.onServerStartButtonPressed())
        txtStartServer.set(constants.txtStartServer)
