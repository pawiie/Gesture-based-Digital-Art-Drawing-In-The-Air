"""
Created on Wed Apr 2021 12 22:35:33 

@author: PS Chauhan
"""

""" It is the main file for tracking the object """


# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import ColourFinder
import logger


# creating object of the log class in logger
OT_log = logger.Log()


#getting the HSV range of colour of the object
CF = ColourFinder.ColourFinder()
LowerHSV,UpperHSV = CF.HSVRange()


#currently not using any multi threading
vs = VideoStream(src=0).start()

# allow the camera or video file to warm up i.e., for camera to open and adjust
time.sleep(2.0)

#loop till we get the feed from camera
while True:
    frame = vs.read()
    
    # if no frame is detected
    if frame == None:
        OT_log.addLog('error','no frames detected')
        break

    # resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame,width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color selected, then perform
	# a series of dilations and erosions to remove any small blobs left in the mask
	mask = cv2.inRange(hsv, LowerHSV, UpperHSV)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    	# update the points queue
    
	pts.appendleft(center)
# pop the cordinates and stream them
    for i in range(1,len(pts)):
        print(pts[i], end=" ")
    

    
#STOPING THE CAMERA FEED

	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
        OT_log.addLog('warning','closing the camera feed')
		break


#stop the camera video stream
vs.stop()

# close all windows
cv2.destroyAllWindows()
