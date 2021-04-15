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


#object of Log class
OT_log = logger.Log()


# creating object of the log class in logger
OT_log = logger.Log()


#getting the HSV range of colour of the object

# CF = ColourFinder.ColourFinder()
# LowerHSV,UpperHSV = CF.HSVRange()


LowerHSV =(29, 86, 6)
UpperHSV =(64, 255, 255)

#currently not using any multi threading
vs = VideoStream(src=0).start()

# allow the camera or video file to warm up i.e., for camera to open and adjust
time.sleep(2.0)

pts=deque()
#loop till we get the feed from camera
while True:
    frame = vs.read()
    
    # to counter the mirror effect 
    frame = cv2.flip(frame,1)

    # if no frame is detected
    if frame is None:
        OT_log.addLog('error','no frames detected')
        break

    # resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame,width=600)
    blurred = cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    # construct a mask for the color selected, then perform
	# a series of dilations and erosions to remove any small blobs left in the mask
	
    mask = cv2.inRange(hsv, LowerHSV, UpperHSV)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
	
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
        
        # only proceed if the radius meets a minimum size
        # not needed 
        # if radius > 0:
		# 	# draw the circle and centroid on the frame,
		# 	# then update the list of tracked points
        #     cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
        #     cv2.circle(frame, center, 5, (0, 0, 255), -1)

    	# update the points queue
    
    pts.append(center)

    # for i in range(1, len(pts)):
    #    #if either of the tracked points are None, ignore them
    #     if pts[i - 1] is None or pts[i] is None:
    #        continue
	# 	# otherwise, compute the thickness of the line and
	# 	# draw the connecting lines
    #     print("pts: ", pts[i-1], pts[i])
    #     thickness = int(5)
    #     cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    #     #pts.popleft()
	# # shows the frame to our screen
    # cv2.imshow("Frame", frame)


# pop the cordinates and stream them
    while len(pts)>1:
        a=pts.popleft()
        b=pts[0]
        if a is None or b is None:
            continue
        print("pts: ", a, b)
        thickness = int(5)
        cv2.line(frame, b, a, (0, 0, 255), thickness)
    cv2.imshow("Frame", frame)
    

    
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


