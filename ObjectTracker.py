""" It is the main file for tracking the object
"""


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
