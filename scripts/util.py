import time
import os
import shutil
import datetime
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import messagebox
import constants


def log(*s):
    print(s)

def capture():
    constants.cache = False
    constants.camera.capture("/home/pi/Desktop/IDEX/tmp/raw.jpg")
    os.system("convert -units PixelsPerInch /home/pi/Desktop/IDEX/tmp/raw.jpg -density 300 /home/pi/Desktop/IDEX/tmp/img.jpg")

def openCamera(enableStream=False):
    import picamera
    if constants.cameraEnabled:
        print("Opening camera when already open!")
        return
    constants.streamEnabled = enableStream
    constants.camera = picamera.PiCamera()
    constants.cameraEnabled = True
    constants.camera.rotation = 90
    constants.camera.resolution = (640, 480)
    constants.camera.framerate=60
    if constants.streamEnabled:
        import picamera.array
        constants.raw = picamera.array.PiRGBArray(constants.camera, size=(640, 480))
        constants.vstream = constants.camera.capture_continuous(constants.raw, format="bgr", use_video_port=True)

def closeCamera():
    if not constants.cameraEnabled:
        print("Closing camera when already closed!")
        return
    constants.cameraEnabled = False
    constants.camera.close()
    if constants.streamEnabled:
        constants.raw.truncate()
        constants.raw.seek(0)

def getStreamFrame():
    if constants.cameraEnabled:
        constants.raw.truncate()
        constants.raw.seek(0)
        img = constants.vstream.__next__().array
        return img
    else:
        print("Trying to read frame when camera is not enabled!")
        return None

def ocrtts():
    if not constants.cache:
        os.system("bash /home/pi/Desktop/IDEX/scripts/idex.sh ocr")
        constants.cache = True
    readText()

def ttsdirect(s):
    if len(s.strip()) > 0:
        os.system("bash /home/pi/Desktop/IDEX/scripts/idex.sh ttsdirect \"{0}\"".format(s))


def readText():
    text = open("/home/pi/Desktop/IDEX/tmp/output.txt", "r").read()
    text = text.strip()
    if len(text) > 0:
        log(text)
        constants.filename = "/home/pi/Desktop/IDEX/tmp/output.txt"
        readFile()
    else:
        messagebox.showerror("LEXAID", "No text detected! Steady the device or improve lighting.")
        log("No text found!")


def selectFile():
    global filename
    filename = askopenfilename(initialdir="/media/pi", title="Select file")
    constants.btnSelect.configure(text=filename)
    constants.btnSelect.text = filename
    log(filename)

def trimStr(text):
    return os.linesep.join([s for s in text.splitlines() if s]).strip()

def readFile():
    try:
        file = open(constants.filename, "r")
        text = trimStr(file.read())
        if len(text) == 0:
            messagebox.showerror("LEXAID", "No text detected!")
        else:
            os.system(
                "bash /home/pi/Desktop/IDEX/scripts/idex.sh convert \"{0}\" \"/home/pi/Desktop/IDEX/tmp/ebook.txt\"".format(
                    constants.filename))
            os.system("bash /home/pi/Desktop/IDEX/scripts/idex.sh tts \"{0}\"".format(constants.filename))
        if constants.DEBUG:
            messagebox.showinfo("Debug", text)
    except Exception as exc:
        log(str(exc))


def selectDir(copy=True):
    file = askdirectory(initialdir="/media/pi", title="Select directory")
    ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H-%M-%S")
    fn = file + "/output " + ts + ".txt"
    print("Save directory: ", file)
    print("Save file: ", fn)
    if copy:
        shutil.copy2("/home/pi/Desktop/IDEX/tmp/output.txt", fn)
        os.system(
            "bash /home/pi/Desktop/IDEX/scripts/idex.sh convert \"/home/pi/Desktop/IDEX/tmp/output.txt\" \"{0}\"".format(
                fn))
    else:
        constants.saveDir = file
