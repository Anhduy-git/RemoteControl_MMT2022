
from socket import AF_INET, socket, SOCK_STREAM

from tkinter import filedialog

from PIL import ImageTk, Image
from PIL import Image
import constants


class ClientFeatures:
    client = None
    serverConnectedIP = ""
    
    class KeystrokeMain:
        logger = ''
        PrsHook = False
        PrsUnhook = False

        @classmethod
        def ReceiveHook(cls):
            data = ClientFeatures.client.recv(1024).decode("utf-8")
            string = data
            ClientFeatures.client.sendall(bytes(data, "utf-8"))
            return string

        @classmethod
        def HookKey(cls):
            if cls.PrsHook:
                return
            cls.PrsHook = True
            cls.PrsUnhook = False
            ClientFeatures.client.sendall(bytes("HookKey", "utf-8"))
            checkdata = ClientFeatures.client.recv(1024).decode("utf-8")

        @classmethod
        def UnhookKey(cls):

            if cls.PrsHook:
                ClientFeatures.client.sendall(bytes("UnhookKey", "utf-8"))
                cls.logger = cls.ReceiveHook()
                ClientFeatures.client.sendall(bytes(cls.logger, "utf-8"))
                cls.PrsUnhook = True
                cls.PrsHook = False

        @classmethod
        def PrintKey(cls):
            if not cls.PrsUnhook:
                ClientFeatures.client.sendall(bytes("UnhookKey", "utf-8"))
                cls.logger = cls.ReceiveHook()
            # delete(1.0, END)
            # insert(1.0, logger)
            cls.PrsUnhook = True
            cls.PrsHook = False
            
            return cls.logger

    @classmethod
    def WatchTask_PROCESS(cls):

        if cls.client == None:
            return None

        length = 0
        ID = [''] * 10000
        Name = [''] * 10000
        Thread = [''] * 10000
        try:
            cls.client.sendall(bytes("ProcessRunning", "utf-8"))
        except:
            print("Warning !", "Connection error ")
        # Receive data
        try:
            length = cls.client.recv(1024).decode("utf-8")
            length = int(length)

            for i in range(length):
                data = cls.client.recv(1024).decode("utf-8")
                ID[i] = data
                cls.client.sendall(bytes(data, "utf-8"))

            for i in range(length):
                data = cls.client.recv(1024).decode("utf-8")
                Name[i] = data
                cls.client.sendall(bytes(data, "utf-8"))

            for i in range(length):
                data = cls.client.recv(1024).decode("utf-8")
                Thread[i] = data
                cls.client.sendall(bytes(data, "utf-8"))

            for i in range(length):
                print(Name[i] + "\n\n\n\n" + ID[i] + "\n\n" + Thread[i])

            return ID, Name, Thread
        except:
            print("Warning !", "Connection error ")
            return None

    @classmethod
    def WatchTask_APP(cls):
        if (cls.client == None):
            return None

        length = 0  # Danh sách các app đang chạy
        ID = [''] * 100  # Mảng lưu ID của app
        Name = [''] * 100  # Lưu tên app
        Thread = [''] * 100  # lưu luồng
        try:
            cls.client.sendall(bytes("AppRunning", "utf-8"))
        except:

            print("Warning !", "Connection error ")

        # Receive data
        try:
            length = cls.client.recv(1024).decode("utf-8")
            length = int(length)
            for i in range(length):
                data = cls.client.recv(1024).decode("utf-8")
                ID[i] = data
                cls.client.sendall(bytes(data, "utf-8"))

            for i in range(length):
                data = cls.client.recv(1024).decode("utf-8")
                Name[i] = data
                cls.client.sendall(bytes(data, "utf-8"))

            for i in range(length):
                data = cls.client.recv(1024).decode("utf-8")
                Thread[i] = data
                cls.client.sendall(bytes(data, "utf-8"))

            for i in range(length):
                print(Name[i] + "\n\n\n\n" + ID[i] + "\n\n" + Thread[i])
            return ID, Name, Thread
        except:
            print("Warning !", "Connection error ")
            return None
    @classmethod
    def KillTask(cls, pid):
        def Kill():
            cls.client.sendall(bytes("KillTask", "utf-8"))
            try:
                cls.client.sendall(bytes(pid, "utf-8"))
                checkdata = cls.client.recv(1024).decode("utf-8")
                if (checkdata == "Killed"):
                    print("", "Killed the program")
                else:
                    print("", "No program found")
            except:
                print("", "No program found")

        Kill()

    @classmethod
    def StartTask(cls, name):
        def Start():

            cls.client.sendall(bytes("StartTask", "utf-8"))
            try:
                cls.client.sendall(bytes(name, "utf-8"))
                checkdata = cls.client.recv(1024).decode("utf-8")
                if (checkdata == "Started"):
                    print("", "The program is on")
                else:
                    print("", "No program found")
            except:
                print("", "No program found")

        Start()

    ##############################################
    @classmethod
    def Shutdown(cls):
        try:
            cls.client.send(bytes("Shutdown", 'utf-8'))

        except:
            print(" ", "Connection error")

    ##############################################
    @classmethod
    def ReceivePicture(cls):  # Nhận ảnh từ server
        try:
            cls.client.sendall(bytes("TakePicture", "utf-8"))
        except:
            print(" ", "Connection error")

        file = open("Resources/image.png", 'wb')
        data = cls.client.recv(40960000)
        file.write(data)
        img = ImageTk.PhotoImage(Image.open("Resources/image.png"))
        file.close()

    @classmethod
    def SavePicture(cls):
        myScreenShot = open("Resources/image.png", 'rb')
        data = myScreenShot.read()
        fname = filedialog.asksaveasfilename(title=u'Save file', filetypes=[("PNG", ".png")])
        myScreenShot.close()
        if fname.strip() != '':
            file = open(str(fname) + '.png', 'wb')
            file.write(data)
            file.close()

    @classmethod
    def connectServer(cls, HOST):
        global Host
        Host = HOST
        cls.client = socket(AF_INET, SOCK_STREAM)
        try:
            cls.client.connect((HOST, constants.PORT))
            cls.client.send(bytes("Success", 'utf-8'))
            cls.serverConnectedIP = HOST
            return True
        except:
            print("Warning!!!", "Connection error ")
            return False

