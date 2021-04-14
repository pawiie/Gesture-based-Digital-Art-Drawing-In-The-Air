#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 22:35:33 2021

@author: pawansinghchauhan
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
        
        break
