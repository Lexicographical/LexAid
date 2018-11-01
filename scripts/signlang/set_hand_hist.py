import cv2
import numpy as np
import pickle
import constants
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import util

cam = None
x, y, w, h = 300, 100, 300, 300
flagPressedC, flagPressedS = False, False
imgCrop = hist = None
pic = vstream = raw = None


def build_squares(img):
	x, y, w, h = 420, 140, 10, 10
	d = 10
	imgCrop = None
	x1, y1 = x, y
	for i in range(10):
		for j in range(5):
			if np.any(imgCrop is None):
				imgCrop = img[y:y + h, x:x + w]
			else:
				imgCrop = np.vstack((imgCrop, img[y:y + h, x:x + w]))
			x += w + d
		x = 420
		y += h + d
	cv2.rectangle(img, (x1, y1), (x1 + (w + d) * 5, y1 + (h + d) * 10), (0, 255, 0), 2)
	return imgCrop

def get_hand_hist():
	global cam
	if not constants.PI:
		cam = cv2.VideoCapture(constants.camera_driver)
	else:
		util.openCamera(True)
	render()

def render():
	global cam, flagPressedC, flagPressedS, imgCrop, hist, pic
	if not constants.PI and cam is None:
		print("Null camera")
	if constants.PI:
		img = util.getStreamFrame()
		if img is None:
			return
	else:
		img = cam.read()[1]
		img = cv2.flip(img, 1)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	thresh = None
	if constants.pressedKey == "c":
		constants.pressedKey = None
		print("recalibrate")
		hsvCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2HSV)
		flagPressedC = True
		hist = cv2.calcHist([hsvCrop], [0, 1], None, [180, 256], [0, 180, 0, 256])
		cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
		constants.calibrated = True
	elif constants.pressedKey == "s":
		if constants.calibrated:
			print("Stopped cam")
			if not constants.PI:
				cam.release()
			else:
				util.closeCamera()
			cv2.destroyAllWindows()
			constants.pressedKey = None
			with open("hist", "wb")as f:
				pickle.dump(hist, f)
			return
		else:
			constants.pressedKey = None
			messagebox.showerror("LexAid", "Please calibrate your hand first.")
	if flagPressedC:
		dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)
		disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
		cv2.filter2D(dst, -1, disc, dst)
		blur = cv2.GaussianBlur(dst, (11, 11), 0)
		blur = cv2.medianBlur(blur, 15)
		ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		thresh = cv2.merge((thresh, thresh, thresh))
		res = cv2.bitwise_and(img, thresh)
		# cv2.imshow("res", res)
	if not flagPressedS:
		imgCrop = build_squares(img)
	if constants.streamState or not flagPressedC:
		pic = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		build_squares(pic)
	else:
		cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
		build_squares(thresh)
		pic = thresh
	timg = Image.fromarray(pic).resize(constants.stream_dimens, Image.ANTIALIAS)
	timgtk = ImageTk.PhotoImage(image = timg)
	constants.lblHandHistStream.imgtk = timgtk
	constants.lblHandHistStream.configure(image = timgtk)
	constants.lblHandHistStream.after(1, render)