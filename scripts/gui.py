from PIL import ImageTk, Image
import util
import constants
import os
import sys
from tkinter import Tk, Grid, Frame, Button, Label, messagebox

sys.path.insert(0, "signlang")
import set_hand_hist
import fun_util

preview_dim = (480, 160)

def togglePreview(enabled = True):
    if constants.DEBUG and constants.DESKTOP:
        return
    if enabled:
        os.system("fbcp &")
        constants.camera.start_preview(fullscreen = True)
    else:
        constants.camera.stop_preview()
        os.system("killall fbcp")


def capture():
    util.capture()
    switchLayout(constants.MAIN)


def destroy():
    os.system("killall fbcp")
    constants.root.destroy()

def toggleDebug():
    constants.DEBUG = not constants.DEBUG
    constants.btnDebugMode.configure(text = "Debug mode: " + str(constants.DEBUG))


def switchLayout(n):
    if n == constants.CAPTURE:
        if not constants.cameraEnabled:
            util.openCamera()
        togglePreview(True)
    else:
        if constants.cameraEnabled:
            togglePreview(False)
            util.closeCamera()
    if n == constants.MAIN:
        constants.img = ImageTk.PhotoImage(
            Image.open("../tmp/img.jpg").resize(preview_dim, Image.ANTIALIAS))
        constants.lblImg.configure(image = constants.img)
    constants.frames[n].tkraise()
    if n == constants.HANDHIST:
        set_hand_hist.get_hand_hist()
    elif n == constants.VISION:
        fun_util.recognize()


def buildOther():
    frameOther = Frame(constants.root)
    frameOther.grid(row = 0, column = 0, sticky = "nsew")

    constants.btnSelect = Button(frameOther, text = "Select file...", command = util.selectFile, borderwidth = 1, 
                                 relief = "solid")
    constants.btnSelect.grid(row = 0, column = 0, sticky = "nsew")
    btnRead = Button(frameOther, text = "Read", command = util.readFile, borderwidth = 1, relief = "solid")
    btnRead.grid(row = 1, column = 0, sticky = "nsew")
    btnMenu = Button(frameOther, text = "Main Menu", command = lambda:switchLayout(constants.MAIN), borderwidth = 1, 
                     relief = "solid")
    btnMenu.grid(row = 2, column = 0, sticky = "nsew")

    for i in range(3):
        Grid.rowconfigure(frameOther, i, weight = 1)
    for j in range(1):
        Grid.columnconfigure(frameOther, j, weight = 1)

    constants.frames[constants.OTHER] = frameOther


def buildCapture():
    frameCapture = Frame(constants.root)
    frameCapture.grid(row = 0, column = 0, sticky = "nsew")
    btnCapture = Button(frameCapture, text = "Capture", command = capture, borderwidth = 1, relief = "solid")
    btnCapture.grid(row = 0, column = 0, sticky = "nsew", padx = 5, pady = 5)
    Grid.rowconfigure(frameCapture, 0, weight = 1)
    Grid.columnconfigure(frameCapture, 0, weight = 1)
    constants.frames[constants.CAPTURE] = frameCapture


def buildMain():
    frameMain = Frame(constants.root)
    frameMain.grid(row = 0, column = 0, sticky = "nsew")

    constants.img = ImageTk.PhotoImage(
        Image.open("../tmp/img.jpg").resize(preview_dim, Image.ANTIALIAS))
    constants.lblImg = Label(frameMain, image = constants.img)
    constants.lblImg.grid(row = 0, column = 0, columnspan = 4, sticky = "nsew")

    btnCapture = Button(frameMain, image = constants.imgCamera, command = lambda:switchLayout(constants.CAPTURE), relief = "flat")
    btnCapture.grid(row = 1, column = 0, columnspan = 4, sticky = "nsew", padx = 5, pady = 5)

    btnRead = Button(frameMain, image = constants.imgRead, command = util.ocrtts, relief = "flat")
    btnRead.grid(row = 2, column = 0, sticky = "nsew")
    btnSave = Button(frameMain, image = constants.imgSave, command = util.selectDir, relief = "flat")
    btnSave.grid(row = 2, column = 1, sticky = "nsew")
    btnOther = Button(frameMain, text = "Other", command = lambda:switchLayout(constants.OTHER), relief = "flat")
    btnOther.grid(row = 2, column = 2, sticky = "nsew")
    btnExit = Button(frameMain, image = constants.imgExit, command = lambda:switchLayout(constants.HOME), relief = "flat")
    btnExit.grid(row = 2, column = 3, sticky = "nsew")

    for i in range(3):
        Grid.rowconfigure(frameMain, i, weight = 1)
    for j in range(4):
        Grid.columnconfigure(frameMain, j, weight = 1)
    constants.frames[constants.MAIN] = frameMain

def buildSettings():
    frameSettings = Frame(constants.root)
    frameSettings.grid(row = 0, column = 0, sticky = "nsew")

    constants.btnDebugMode = Button(frameSettings, text = "Debug mode: " + str(constants.DEBUG), command = toggleDebug, relief = "solid", borderwidth = 1)
    constants.btnDebugMode.grid(row = 0, column = 0, sticky = "nsew")

    btnExit = Button(frameSettings, image = constants.imgExit, command = lambda:switchLayout(constants.HOME), relief = "flat")
    btnExit.grid(row = 1, column = 0, sticky = "nsew")

    for i in range(2):
        Grid.rowconfigure(frameSettings, i, weight = 1)
    Grid.columnconfigure(frameSettings, 0, weight = 1)

    constants.frames[constants.SETTINGS] = frameSettings

def toVision():
    if constants.saveDir is None and not constants.DEBUG:
        messagebox.showerror("LexAid", "No save directory selected! Please select one first.")
        print("Error, constants.saveDir is None")
    else:
        switchLayout(constants.VISION)

def buildVisionHome():
    frameVisionHome = Frame(constants.root)
    frameVisionHome.grid(row = 0, column = 0, sticky = "nsew")

    btnBack = Button(frameVisionHome, image = constants.imgExit, command = lambda:switchLayout(constants.HOME), relief = "flat")
    btnBack.grid(row = 0, column = 0, columnspan=2, sticky = "nsew")

    btnSelect = Button(frameVisionHome, image = constants.imgSave, command = lambda:util.selectDir(False), relief = "flat")
    btnSelect.grid(row = 1, column = 0, columnspan=2, sticky = "nsew")

    btnStart = Button(frameVisionHome, image = constants.imgCamera, command = toVision, relief = "flat")
    btnStart.grid(row = 2, column = 0, sticky = "nsew")

    btnHandHist = Button(frameVisionHome, image=constants.imgHand, command=lambda: switchLayout(constants.HANDHIST), relief="flat")
    btnHandHist.grid(row=2, column=1, sticky="nsew")
    
    for i in range(3):
        Grid.rowconfigure(frameVisionHome, i, weight = 1)
    Grid.columnconfigure(frameVisionHome, 0, weight = 1)
    Grid.columnconfigure(frameVisionHome, 1, weight = 1)
    
    constants.frames[constants.VISIONHOME] = frameVisionHome

def buildVision():
    frameVision = Frame(constants.root)
    frameVision.grid(row = 0, column = 0, sticky = "nsew")

    btnBack = Button(frameVision, image = constants.imgExit, command = lambda: press("s"), relief = "flat")
    btnBack.grid(row = 0, column = 0, sticky = "nsew")

    btnToggle = Button(frameVision, image=constants.imgSettings, command=lambda: press("t"), relief="flat")
    btnToggle.grid(row=0, column=1, sticky="nsew")

    constants.lblUtilStream = Label(frameVision)
    constants.lblUtilStream.grid(row=1, column=0, columnspan=2)

    for i in range(2):
        Grid.rowconfigure(frameVision, i, weight = 1)
    for i in range(2):
        Grid.columnconfigure(frameVision, i, weight = 1)

    constants.frames[constants.VISION] = frameVision

def press(s):
    if s == "t":
        constants.streamState = not constants.streamState
        return
    constants.pressedKey = s
    if s == "s":
        if constants.calibrated:
            switchLayout(constants.VISIONHOME)

def buildHandHist():
    frameHandHist = Frame(constants.root)
    frameHandHist.grid(row = 0, column = 0, sticky = "nsew")

    btnS = Button(frameHandHist, image=constants.imgSave, command = lambda: press("s"), relief = "solid", borderwidth=1)
    btnS.grid(row = 0, column = 0, sticky = "nsew")

    btnT = Button(frameHandHist, image=constants.imgToggle, command= lambda: press("t"), relief = "solid", borderwidth=1)
    btnT.grid(row=0, column=1, stick="nsew")

    btnC = Button(frameHandHist, image=constants.imgCheck, command = lambda: press("c"), relief = "solid", borderwidth=1)
    btnC.grid(row = 0, column = 2, sticky = "nsew")

    constants.lblHandHistStream = Label(frameHandHist)
    constants.lblHandHistStream.grid(row=1, column=0, columnspan=3)

    for i in range(2):
        Grid.rowconfigure(frameHandHist, i, weight = 1)
    for i in range(3):
        Grid.columnconfigure(frameHandHist, i, weight = 1)

    constants.frames[constants.HANDHIST] = frameHandHist


def buildHome():
    frameHome = Frame(constants.root)
    frameHome.grid(row = 0, column = 0, sticky = "nsew")

    btnExit = Button(frameHome, image = constants.imgExit, command = destroy, relief = "flat")
    btnExit.grid(row = 0, column = 3, sticky = "nsew")

    lblLogo = Label(frameHome, image = constants.imgLogo)
    lblLogo.grid(row = 1, column = 0, sticky = "nsew", columnspan = 4)

    if not constants.DESKTOP:
        btnStart = Button(frameHome, image = constants.imgCamera, command = lambda:switchLayout(constants.CAPTURE), 
                       relief = "flat")
        btnStart.grid(row = 2, column = 2, sticky = "nsew", columnspan = 2)

    btnVision = Button(frameHome, image = constants.imgHand, command = lambda:switchLayout(constants.VISIONHOME), relief = "flat")
    btnVision.grid(row = 2, column = 0, sticky = "nsew", columnspan = 4 if constants.DESKTOP else 2)

    # if constants.DEBUG:
    #     btnSound = Button(frameHome, image = constants.imgSettings, command = lambda:switchLayout(constants.SETTINGS), 
    #                     relief = "flat")
    #     btnSound.grid(row = 3, column = 1, sticky = "nsew", columnspan = 2)

    for i in range(4):
        Grid.rowconfigure(frameHome, i, weight = 1)
    for i in range(4):
        Grid.columnconfigure(frameHome, i, weight = 1)

    constants.frames[constants.HOME] = frameHome

def initPics():
    constants.imgExit = ImageTk.PhotoImage(Image.open("../misc/exit.png").resize((32, 32), Image.ANTIALIAS))
    constants.imgLogo = ImageTk.PhotoImage(Image.open("../misc/logo.png").resize((264, 200) if constants.PI else (428, 240), Image.ANTIALIAS))
    constants.imgCamera = ImageTk.PhotoImage(Image.open("../misc/camera.png").resize((64, 64), Image.ANTIALIAS))
    constants.imgSettings = ImageTk.PhotoImage(Image.open("../misc/settings.png").resize((64, 64), Image.ANTIALIAS))
    constants.imgRead = ImageTk.PhotoImage(Image.open("../misc/read.png").resize((64, 64), Image.ANTIALIAS))
    constants.imgSave = ImageTk.PhotoImage(Image.open("../misc/save.png").resize((64, 64), Image.ANTIALIAS))
    constants.imgHand = ImageTk.PhotoImage(Image.open("../misc/hand.png").resize((64, 64), Image.ANTIALIAS))
    constants.imgCheck = ImageTk.PhotoImage(Image.open("../misc/check.png").resize((64, 64), Image.ANTIALIAS))
    constants.imgToggle = ImageTk.PhotoImage(Image.open("../misc/toggle.png").resize((64, 64), Image.ANTIALIAS))

def buildGUI():
    root = Tk()
    root.resizable(width = False, height = False)
    root.geometry("480x320")
    # if not constants.DEBUG:
    root.attributes("-fullscreen", True)
    if os.name == "nt":
        root.iconbitmap(bitmap = os.path.abspath("../misc/icon.ico"))
    else:
        root.iconbitmap(bitmap = "@" + os.path.abspath("../misc/icon.xbm"))

    root.grid_rowconfigure(0, weight = 1)
    root.grid_columnconfigure(0, weight = 1)
    constants.root = root
    if constants.start:
        initPics()
        buildOther()
        buildMain()
        buildCapture()
        if constants.DEBUG:
            buildSettings()
        buildVisionHome()
        buildVision()
        buildHandHist()
        buildHome()
        constants.start = False
        constants.root.mainloop()
