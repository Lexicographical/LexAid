from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, askdirectory

root = None
start = True
frames = [0 for i in range(2)]
filename = None

def destroy():
    global root
    root.destroy()

def capture():
	print("Captured")
	
def ocrtts():
	print("Reading")

def switchLayout(n):
    frames[n].tkraise()

def selectFile():
    global filename
    filename = askopenfilename()
    print(filename)

def readFile():
    global filename
    try :
        file = open(filename, "r")
        text = file.read()
        print(text)
    except:
        print("Could not read file!")

def selectDir():
    file = askdirectory()
    print(file)


def buildOther():
    global root, frames
    frameOther = Frame(root)
    frameOther.grid(row=0, column=0, sticky=W+E+N+S)

    btnSelect = Button(frameOther, text="Select file...", command=selectFile, borderwidth=1, relief="solid")
    btnSelect.grid(row=0, column=0, sticky=W+E+N+S)
    btnRead = Button(frameOther, text="Read", command=readFile, borderwidth=1, relief="solid")
    btnRead.grid(row=1, column=0, sticky=W+E+N+S)
    btnMenu = Button(frameOther, text="Main Menu", command=lambda: switchLayout(0), borderwidth=1, relief="solid")
    btnMenu.grid(row=2, column=0, sticky=W+E+N+S)

    for i in range(3):
        Grid.rowconfigure(frameOther, i, weight=1)
    for j in range(1):
        Grid.columnconfigure(frameOther, j, weight=1)

    frames[1] = frameOther

def buildMain():
    global root, frames
    frameMain = Frame(root)
    frameMain.grid(row=0, column=0, sticky=W+E+N+S)

    img = ImageTk.PhotoImage(Image.open("img.jpg").resize((240, 320), Image.ANTIALIAS))
    lblImg = Label(frameMain, image=img)
    lblImg.grid(row=0, column=0, rowspan=4, sticky=W+E+N+S)

    btnCapture = Button(frameMain, text="Capture", command=capture, borderwidth=1, relief="solid")
    btnCapture.grid(row=4, column=0, sticky=W+E+N+S, padx=5, pady=5)
    
    btnRead = Button(frameMain, text="Read", command=ocrtts, borderwidth=1, relief="solid")
    btnRead.grid(row=0, column=1, sticky=W+E+N+S, padx=5, pady=5)
    btnSave = Button(frameMain, text="Save", command=selectDir, borderwidth=1, relief="solid")
    btnSave.grid(row=1, column=1, sticky=W+E+N+S, padx=5, pady=5)
    btnOther = Button(frameMain, text="Other", command=lambda: switchLayout(1), borderwidth=1, relief="solid")
    btnOther.grid(row=2, column=1, sticky=W+E+N+S, padx=5, pady=5)
    btnExit = Button(frameMain, text="Exit", command=destroy, borderwidth=1, relief="solid")
    btnExit.grid(row=3, column=1, sticky=W+E+N+S, padx=5, pady=5)
    
    for i in range(4):
        Grid.rowconfigure(frameMain, i, weight=1)
    for j in range(2):
        Grid.columnconfigure(frameMain, j, weight=1)
    frames[0] = frameMain
    root.mainloop()

def buildGUI():
    global root, start
    root = Tk()
    root.resizable(width=False, height=False)
    root.geometry("480x320")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    if start:
        buildOther()
        buildMain()
        start = False

buildGUI()
