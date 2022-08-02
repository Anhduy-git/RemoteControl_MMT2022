import tkinter as tk
import socket
import constants
from serverFeatures import ServerFeatures


class Server:
    def __init__(self, root):
        self.root = root
        self.startServerBtn = None
        self.txtStartServer = None

    def onServerStartButtonPressed(self):
        ServerFeatures.setUpServer()


    def onCreate(self):
        # init frame
        self.frame = tk.Frame(self.root, bg=constants.bgColor)
        self.frame.place(relwidth=1, relheight=1)

        # button click menu
        self.txtStartServer = tk.StringVar()
        self.startServerBtn = tk.Button(self.frame, textvariable=self.txtStartServer, font=constants.mainFont, bg="#20bebe",
                                        fg="white")
        self.startServerBtn.place(x=50, y=50, relwidth=1, relheight=1, width=-100, height=-100)
        self.startServerBtn.config(command=lambda: self.onServerStartButtonPressed())
        self.txtStartServer.set(constants.txtStartServer + '\nServer IP: ' + socket.gethostbyname(socket.gethostname()))
