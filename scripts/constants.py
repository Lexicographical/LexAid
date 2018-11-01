
root = None
frames = [0 for i in range(8)]
lblImg = btnSelect = btnDebugMode = img = None
imLog = imgExit = imgCamera = imgSettings = imgRead = imgSave = imgHand = imgCheck = imgToggle = None
pressedKey = None
saveDir = None
start = True
cache = True
DEBUG = True
lblHandHistStream = None
lblUtilStream = None
streamState = True
calibrated = False
DESKTOP = True
PI = False
camera = raw = vstream = None
cameraEnabled = streamEnabled = False

try:
    import picamera, picamera.array
    PI = True
except ImportError:
    print("picamera not found. Debug mode activated.");
filename = None

if PI:
    stream_dimens = (264, 200)
else:
    stream_dimens = (800, 500)

HOME = 0
CAPTURE = 1
MAIN = 2
OTHER = 3
SETTINGS = 4
VISIONHOME = 5
VISION = 6
HANDHIST = 7

# signlang
camera_driver = 0