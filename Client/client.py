try:
    import tkinter as tk
    from tkinter import ttk
    import constants
    from clientFeatures import ClientFeatures
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pillow"]
    call("pip install " + ' '.join(modules), shell=True)


class Client:
    def __init__(self, root):
        self.root = root



    def onServerConnectButtonPressed(self):
        serverIP = self.inputIPBox.get("1.0", 'end-1c')
        if (ClientFeatures.connectServer(serverIP)):
            # pop up a window succcess
            popupRoot = tk.Tk()
            canvas = tk.Canvas(popupRoot, width=constants.POPUP_WIDTH, height=constants.POPUP_HEIGHT)
            canvas.pack()
            popupFrame = tk.Frame(popupRoot, bg=constants.bgColor)
            popupFrame.place(relwidth=1, relheight=1)
            txtInformation = tk.Label(popupRoot, text=constants.txtConnectSuccess, font=(constants.mainFont, 20))
            txtInformation.config(bg=constants.bgColor)
            txtInformation.place(x=20,y=50)
            popupRoot.mainloop()
        else:
            # pop up a window failed
            popupRoot = tk.Tk()
            canvas = tk.Canvas(popupRoot, width=constants.POPUP_WIDTH, height=constants.POPUP_HEIGHT)
            canvas.pack()
            popupFrame = tk.Frame(popupRoot, bg=constants.bgColor)
            popupFrame.place(relwidth=1, relheight=1)
            txtInformation = tk.Label(popupRoot, text=constants.txtConnectFailed, font=(constants.mainFont, 25))
            txtInformation.config(bg=constants.bgColor)
            txtInformation.place(x=50, y=50)
            popupRoot.mainloop()


    def onScreenshotButtonPressed(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        Screenshot(self.root).onCreate()

    def onProcessRunningButtonPressed(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        ProcessRunning(self.root).onCreate()

    def onAppRunningButtonPressed(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        AppRunning(self.root).onCreate()

    def onKeystrokeButtonPressed(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        Keystroke(self.root).onCreate()

    def onShutdownButtonPressed(self):
        ClientFeatures.Shutdown()

    def onCloseButtonPressed(self):
        self.root.destroy()
    def onCreate(self):

        # init frame
        self.frame = tk.Frame(self.root, bg=constants.bgColor)
        self.frame.place(relwidth=1, relheight=1)

        # input IP text box
        self.inputIPBox = tk.Text(self.frame)
        self.inputIPBox.place(x=20, y=20, width=400, height=30)
        # set IP of server
        self.inputIPBox.insert("end-1c", ClientFeatures.serverConnectedIP)


        # button connect
        txtConnectServer = tk.StringVar()
        self.connectServerBtn = tk.Button(self.frame, textvariable=txtConnectServer, font=constants.mainFont,
                                          bg="#20bebe", fg="white")
        self.connectServerBtn.place(x=430, y=20, width=100, height=30)
        self.connectServerBtn.config(command=lambda: self.onServerConnectButtonPressed())
        txtConnectServer.set(constants.txtConnectServer)

        # button Process running
        txtProcessRunning = tk.StringVar()
        self.processRunningBtn = tk.Button(self.frame, textvariable=txtProcessRunning, font=constants.mainFont,
                                          bg="#20bebe", fg="white")
        self.processRunningBtn.place(x=20, y=100, width=100, height=250)
        self.processRunningBtn.config(command=lambda: self.onProcessRunningButtonPressed())
        txtProcessRunning.set(constants.txtProcessRunning)

        # button app running
        txtAppRunning = tk.StringVar()
        self.appRunningBtn = tk.Button(self.frame, textvariable=txtAppRunning, font=constants.mainFont,
                                          bg="#20bebe", fg="white")
        self.appRunningBtn.place(x=150, y=100, width=250, height=50)
        self.appRunningBtn.config(command=lambda: self.onAppRunningButtonPressed())
        txtAppRunning.set(constants.txtAppRunning)

        # button keystroke
        txtKeystroke = tk.StringVar()
        self.keystrokeBtn = tk.Button(self.frame, textvariable=txtKeystroke, font=constants.mainFont,
                                          bg="#20bebe", fg="white")
        self.keystrokeBtn.place(x=430, y=100, width=100, height=250)
        self.keystrokeBtn.config(command=lambda: self.onKeystrokeButtonPressed())
        txtKeystroke.set(constants.txtKeystroke)

        # button shutdown
        txtShutdown = tk.StringVar()
        self.shutdownBtn = tk.Button(self.frame, textvariable=txtShutdown, font=constants.mainFont,
                                     bg="#20bebe", fg="white")
        self.shutdownBtn.place(x=150, y=180, width=110, height=60)
        self.shutdownBtn.config(command=lambda: self.onShutdownButtonPressed())
        txtShutdown.set(constants.txtShutdown)

        # button screenshot
        txtScreenshot = tk.StringVar()
        self.screenshotBtn = tk.Button(self.frame, textvariable=txtScreenshot, font=constants.mainFont,
                                          bg="#20bebe", fg="white")
        self.screenshotBtn.place(x=290, y=180, width=110, height=60)
        self.screenshotBtn.config(command=lambda: self.onScreenshotButtonPressed())
        txtScreenshot.set(constants.txtScreenshot)



        # button close
        txtClose = tk.StringVar()
        self.closeBtn = tk.Button(self.frame, textvariable=txtClose, font=constants.mainFont,
                                       bg="#20bebe", fg="white")
        self.closeBtn.place(x=215, y=270, width=120, height=70)
        self.closeBtn.config(command=lambda: self.onCloseButtonPressed())
        txtClose.set(constants.txtClose)


class Screenshot:
    def __init__(self, root):
        self.root = root

    def onBackPressed(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        Client(self.root).onCreate()

    def onScreenshotButtonPressed(self):
        ClientFeatures.ReceivePicture()
        img = Image.open("Resources/image.png")
        resized_img = img.resize(constants.imageSize, Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(resized_img)
        screenshot = tk.Label(self.frame, image=new_img)
        screenshot.photo = new_img
        screenshot.place(x=20, y=70)

    def onCreate(self):
        # init frame
        self.frame = tk.Frame(self.root, bg=constants.bgColor)
        self.frame.place(relwidth=1, relheight=1)

        # button take screenshot
        txtScreenshot = tk.StringVar()
        self.screenshotBtn = tk.Button(self.frame, textvariable=txtScreenshot, font=constants.mainFont,
                                       bg="#20bebe", fg="white")
        self.screenshotBtn.place(x=450, y=60, width=80, height=200)
        self.screenshotBtn.config(command=lambda: self.onScreenshotButtonPressed())
        txtScreenshot.set(constants.txtScreenshot)

        # button save
        txtSave = tk.StringVar()
        self.saveBtn = tk.Button(self.frame, textvariable=txtSave, font=constants.mainFont,
                                       bg="#20bebe", fg="white")
        self.saveBtn.place(x=450, y=280, width=80, height=60)
        self.saveBtn.config(command=lambda: ClientFeatures.SavePicture())
        txtSave.set(constants.txtSave)

        # back button
        photo = tk.PhotoImage(file=constants.backImagePath)
        self.backBtnPhoto = photo.subsample(10, 10)
        self.backBtn = tk.Button(self.frame, image=self.backBtnPhoto)
        self.backBtn.config(command=lambda: self.onBackPressed())
        self.backBtn.place(x=20, y=20, width=40, height=40)

class ProcessRunning:
    def __init__(self, root):
        self.root = root

    def onBackPressed(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        Client(self.root).onCreate()





    def onKillBtnPressed(self):
        # pop up a window to notify
        popupRoot = tk.Toplevel(self.root)
        popupRoot.title("Kill")
        canvas = tk.Canvas(popupRoot, width=constants.POPUP_WIDTH, height=constants.POPUP_HEIGHT)
        canvas.pack()
        popupFrame = tk.Frame(popupRoot, bg=constants.bgColor)
        popupFrame.place(relwidth=1, relheight=1)
        # input IP text box
        inputIPBox = tk.Text(popupFrame)
        inputIPBox.place(x=20, y=20, width=180, height=30)

        # button kill
        txtKill = tk.StringVar()
        killBtn = tk.Button(popupFrame, textvariable=txtKill, font=constants.mainFont, bg="#EE0D1B", fg="white")
        killBtn.place(x=210, y=20, width=60, height=30)
        killBtn.config(command=lambda: ClientFeatures.KillTask(inputIPBox.get("1.0", 'end-1c')))
        txtKill.set(constants.txtKill)

    def onStartBtnPressed(self):
        # pop up a window to notify
        popupRoot = tk.Toplevel(self.root)
        popupRoot.title("Start")
        canvas = tk.Canvas(popupRoot, width=constants.POPUP_WIDTH, height=constants.POPUP_HEIGHT)
        canvas.pack()
        popupFrame = tk.Frame(popupRoot, bg=constants.bgColor)
        popupFrame.place(relwidth=1, relheight=1)
        # input name text box
        inputNameBox = tk.Text(popupFrame)
        inputNameBox.place(x=20, y=20, width=180, height=30)

        # button start
        txtStart = tk.StringVar()
        startBtn = tk.Button(popupFrame, textvariable=txtStart, font=constants.mainFont, bg="#20bebe", fg="white")
        startBtn.place(x=210, y=20, width=60, height=30)
        startBtn.config(command=lambda: ClientFeatures.StartTask(inputNameBox.get("1.0", 'end-1c')))
        txtStart.set(constants.txtStart)

    def onWatchBtnPressed(self):
        ID = []
        Name = []
        Thread = []

        if (ClientFeatures.WatchTask_PROCESS() != None):
            ID, Name, Thread = ClientFeatures.WatchTask_PROCESS()

        # add data to the treeview
        for i in range(len(ID)):
            self.treeview.insert('', tk.END, values=(ID[i], Name[i], Thread[i]))

    def onDeleteBtnPressed(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)


    def onCreate(self):
        # init frame
        self.frame = tk.Frame(self.root, bg=constants.bgColor)
        self.frame.place(relwidth=1, relheight=1)

        # button kill
        txtKill = tk.StringVar()
        self.killBtn = tk.Button(self.frame, textvariable=txtKill, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.killBtn.place(x=90, y=20, width=80, height=60)
        self.killBtn.config(command=lambda: self.onKillBtnPressed())
        txtKill.set(constants.txtKill)

        # button watch
        txtWatch = tk.StringVar()
        self.watchBtn = tk.Button(self.frame, textvariable=txtWatch, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.watchBtn.place(x=200, y=20, width=80, height=60)
        self.watchBtn.config(command=lambda: self.onWatchBtnPressed())
        txtWatch.set(constants.txtWatch)

        # button delete
        txtDelete = tk.StringVar()
        self.deleteBtn = tk.Button(self.frame, textvariable=txtDelete, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.deleteBtn.place(x=310, y=20, width=80, height=60)
        self.deleteBtn.config(command=lambda: self.onDeleteBtnPressed())
        txtDelete.set(constants.txtDelete)

        # button start
        txtStart = tk.StringVar()
        self.startBtn = tk.Button(self.frame, textvariable=txtStart, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.startBtn.place(x=420, y=20, width=80, height=60)
        self.startBtn.config(command=lambda: self.onStartBtnPressed())
        txtStart.set(constants.txtStart)

        #scrollbar
        ## create the table
        self.treeview = ttk.Treeview(
            show="headings",
            columns=["Name Process", "ID Process", "Count Thread"])  # table

        # ttk.Style().configure("Treeview.Heading", font=(None, 20))

        self.treeview.column("Name Process", anchor='center', width=100)
        self.treeview.column("ID Process", anchor='center', width=100)
        self.treeview.column("Count Thread", anchor='center', width=100)


        self.treeview.heading("Name Process", text="Name Process")
        self.treeview.heading("ID Process", text="ID Process")
        self.treeview.heading("Count Thread", text="Count Thread")

        print("test")



        self.treeview.place(x=90, y=120, width=400, height=260)

        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=490, y=120, height=260)

        # back button
        photo = tk.PhotoImage(file=constants.backImagePath)
        self.backBtnPhoto = photo.subsample(10, 10)
        self.backBtn = tk.Button(self.frame, image=self.backBtnPhoto)
        self.backBtn.config(command=lambda: self.onBackPressed())
        self.backBtn.place(x=20, y=20, width=40, height=40)

class AppRunning:
    def __init__(self, root):
        self.root = root

    def onBackPressed(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        Client(self.root).onCreate()



    def onKillBtnPressed(self):
        # pop up a window to notify
        popupRoot = tk.Toplevel(self.root)
        popupRoot.title("Kill")
        canvas = tk.Canvas(popupRoot, width=constants.POPUP_WIDTH, height=constants.POPUP_HEIGHT)
        canvas.pack()
        popupFrame = tk.Frame(popupRoot, bg=constants.bgColor)
        popupFrame.place(relwidth=1, relheight=1)
        # input name text box
        inputIPBox = tk.Text(popupFrame)
        inputIPBox.place(x=20, y=20, width=180, height=30)

        # button kill
        txtKill = tk.StringVar()
        killBtn = tk.Button(popupFrame, textvariable=txtKill, font=constants.mainFont, bg="#EE0D1B", fg="white")
        killBtn.place(x=210, y=20, width=60, height=30)
        killBtn.config(command=lambda: ClientFeatures.KillTask(inputIPBox.get("1.0", 'end-1c')))
        txtKill.set(constants.txtKill)

    def onStartBtnPressed(self):
        # pop up a window to notify
        popupRoot = tk.Toplevel(self.root)
        popupRoot.title("Start")
        canvas = tk.Canvas(popupRoot, width=constants.POPUP_WIDTH, height=constants.POPUP_HEIGHT)
        canvas.pack()
        popupFrame = tk.Frame(popupRoot, bg=constants.bgColor)
        popupFrame.place(relwidth=1, relheight=1)
        # input IP text box
        inputNameBox = tk.Text(popupFrame)
        inputNameBox.place(x=20, y=20, width=180, height=30)

        # button start
        txtStart = tk.StringVar()
        startBtn = tk.Button(popupFrame, textvariable=txtStart, font=constants.mainFont, bg="#20bebe", fg="white")
        startBtn.place(x=210, y=20, width=60, height=30)
        startBtn.config(command=lambda: ClientFeatures.StartTask(inputNameBox.get("1.0", 'end-1c')))
        txtStart.set(constants.txtStart)

    def onWatchBtnPressed(self):
        ID = []
        Name = []
        Thread = []

        if (ClientFeatures.WatchTask_APP() != None):
            ID, Name, Thread = ClientFeatures.WatchTask_APP()

        # add data to the treeview
        for i in range(len(ID)):
            self.treeview.insert('', tk.END, values=(ID[i], Name[i], Thread[i]))

    def onDeleteBtnPressed(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)




    def onCreate(self):
        # init frame
        self.frame = tk.Frame(self.root, bg=constants.bgColor)
        self.frame.place(relwidth=1, relheight=1)

        # button kill
        txtKill = tk.StringVar()
        self.killBtn = tk.Button(self.frame, textvariable=txtKill, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.killBtn.place(x=90, y=20, width=80, height=60)
        self.killBtn.config(command=lambda: self.onKillBtnPressed())
        txtKill.set(constants.txtKill)

        # button watch
        txtWatch = tk.StringVar()
        self.watchBtn = tk.Button(self.frame, textvariable=txtWatch, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.watchBtn.place(x=200, y=20, width=80, height=60)
        self.watchBtn.config(command=lambda: self.onWatchBtnPressed())
        txtWatch.set(constants.txtWatch)

        # button delete
        txtDelete = tk.StringVar()
        self.deleteBtn = tk.Button(self.frame, textvariable=txtDelete, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.deleteBtn.place(x=310, y=20, width=80, height=60)
        self.deleteBtn.config(command=lambda: self.onDeleteBtnPressed())
        txtDelete.set(constants.txtDelete)

        # button start
        txtStart = tk.StringVar()
        self.startBtn = tk.Button(self.frame, textvariable=txtStart, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.startBtn.place(x=420, y=20, width=80, height=60)
        self.startBtn.config(command=lambda: self.onStartBtnPressed())
        txtStart.set(constants.txtStart)

        #scrollbar
        ## create the table
        self.treeview = ttk.Treeview(
            show="headings",
            columns=["Name Application", "ID Application", "Count Thread"])  # table

        # ttk.Style().configure("Treeview.Heading", font=(None, 20))

        self.treeview.column("Name Application", anchor='center', width=100)
        self.treeview.column("ID Application", anchor='center', width=100)
        self.treeview.column("Count Thread", anchor='center', width=100)


        self.treeview.heading("Name Application", text="Name Application")
        self.treeview.heading("ID Application", text="ID Application")
        self.treeview.heading("Count Thread", text="Count Thread")



        self.treeview.place(x=90, y=120, width=400, height=260)

        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=490, y=120, height=260)

        # back button
        photo = tk.PhotoImage(file=constants.backImagePath)
        self.backBtnPhoto = photo.subsample(10, 10)
        self.backBtn = tk.Button(self.frame, image=self.backBtnPhoto)
        self.backBtn.config(command=lambda: self.onBackPressed())
        self.backBtn.place(x=20, y=20, width=40, height=40)


class Keystroke:
    def __init__(self, root):
        self.root = root

    def onBackPressed(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        Client(self.root).onCreate()



    def onHookBtnPressed(self):
        ClientFeatures.KeystrokeMain.HookKey()

    def onUnhookBtnPressed(self):
        ClientFeatures.KeystrokeMain.UnhookKey()

    def onPrintBtnPressed(self):
        if (ClientFeatures.KeystrokeMain.PrsHook):
            logger = ClientFeatures.KeystrokeMain.PrintKey()
            self.keystrokeBox.config(state='normal')
            self.keystrokeBox.insert("end-1c", logger)
            self.keystrokeBox.config(state='disabled')

    def onDeleteBtnPressed(self):
        self.keystrokeBox.config(state='normal')
        self.keystrokeBox.delete('1.0', tk.END)
        self.keystrokeBox.config(state='disabled')




    def onCreate(self):
        # init frame
        self.frame = tk.Frame(self.root, bg=constants.bgColor)
        self.frame.place(relwidth=1, relheight=1)

        # button hook
        txtHook = tk.StringVar()
        self.hookBtn = tk.Button(self.frame, textvariable=txtHook, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.hookBtn.place(x=90, y=20, width=80, height=60)
        self.hookBtn.config(command=lambda: self.onHookBtnPressed())
        txtHook.set(constants.txtHook)

        # button watch
        txtUnhook = tk.StringVar()
        self.unhookBtn = tk.Button(self.frame, textvariable=txtUnhook, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.unhookBtn.place(x=200, y=20, width=80, height=60)
        self.unhookBtn.config(command=lambda: self.onUnhookBtnPressed())
        txtUnhook.set(constants.txtUnhook)

        # button print
        txtPrint = tk.StringVar()
        self.printBtn = tk.Button(self.frame, textvariable=txtPrint, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.printBtn.place(x=310, y=20, width=80, height=60)
        self.printBtn.config(command=lambda: self.onPrintBtnPressed())
        txtPrint.set(constants.txtPrint)

        # button delete
        txtDelete = tk.StringVar()
        self.deleteBtn = tk.Button(self.frame, textvariable=txtDelete, font=constants.mainFont,
                                 bg="#20bebe", fg="white")
        self.deleteBtn.place(x=420, y=20, width=80, height=60)
        self.deleteBtn.config(command=lambda: self.onDeleteBtnPressed())
        txtDelete.set(constants.txtDelete)

        # text box keystroke
        self.keystrokeBox = tk.Text(self.frame)
        self.keystrokeBox.place(x=90, y=100, width=410, height=280)
        self.keystrokeBox.config(state='disabled')


        # back button
        photo = tk.PhotoImage(file=constants.backImagePath)
        self.backBtnPhoto = photo.subsample(10, 10)
        self.backBtn = tk.Button(self.frame, image=self.backBtnPhoto)
        self.backBtn.config(command=lambda: self.onBackPressed())
        self.backBtn.place(x=20, y=20, width=40, height=40)

