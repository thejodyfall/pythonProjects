# USAGE
# bird_detector.py
# set up object detection
# if there's an object find out if it's a bird
# if it's a bird save the file

# process_images.py
# load image
# if there's an object find out if it's a bird
# if it is take out foreground and save
# is it a blue tit?

# 


# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils.video import VideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import cv2
import os

# define the paths to the Not Santa Keras deep learning model and
# audio file
MODEL_PATH = "blue_tits.model"

# initialize the total number of frames that *consecutively* contain
# santa along with threshold required to trigger the santa alarm
TOTAL_CONSEC = 0
TOTAL_THRESH = 20

# initialize is the santa alarm has been triggered
SANTA = False
firstFrame = None
frameWidth = 400

# load the model
print("[INFO] loading model...")
model = load_model(MODEL_PATH)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	
	frame = imutils.resize(frame, width=frameWidth)
        orig = frame.copy()

	image = cv2.resize(frame, (28, 28))
	# this is basic is sth there recgonition
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

        objfound = False
        maxX = frameWidth
        maxY = frameWidth
        maxH = 0
        maxW = 0
	# loop over the contours
	for c in cnts:
                objfound = True
                # compute the entire bounding box for all movement
                (x, y, w, h) = cv2.boundingRect(c)
                if x < maxX : maxX = x
                if y < maxY : maxY = y
                maxH = maxH + h
                maxW = maxW + w

        # let's get the object from the background
        # but only if there's sth there!
        if objfound:
                # only draw one rectanlge around everything that's moving
                cv2.rectangle(orig, (maxX, maxY), (maxX + maxW, maxY + maxH), (0, 255, 0), 2)

                image = cv2.resize(frame, (50, 50))
                image = image.astype("float") / 255.0
                image = img_to_array(image)
                image = np.expand_dims(image, axis=0)

                # classify the input image
                (notSanta, santa) = model.predict(image)[0]

                if santa > notSanta:
                        # it's a bird so save the file
                        print("[INFO] object detected...")
                        tempFilename = time.strftime("%Y%m%d-%H%M%S") + '.jpg'
                        # save a copy of the original
                        cv2.imwrite(tempFilename, orig) 

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
vs.stop()
