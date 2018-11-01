import picamera
import os
import time

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV' , '/dev/fb1')

camera = picamera.PiCamera()
camera.start_preview()
time.sleep(5)
camera.stop_preview()