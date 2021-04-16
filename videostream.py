"""
Created on Sat Apr 17 2021 03:17:32

@author: PS Chauhan
"""

""" 
This module is is to create a separate thread for video stream and put frame in queue
to increase the fps
"""

#import necessary packages
from threading import Thread
import cv2


class VideoStream:
    def __init__(self,src=0):

        #initialize video capture
        self.stream = cv2.VideoCapture(src)

        # reading the first frame
        (self.grab,self.frame)=self.stream.read()

        # set variable to stop the streaming
        self.stopped=False


    def start(self):

        # create a thread
        th = Thread(target=self.update, args=())

        #to run in background and end when main program stops
        th.daemon = True
         
        #start the thread
        th.start()
        return self

    def update(self):

        while True:

            # variable is set then stop 
            if self.stopped == True:
                return
            
            #read the next frame
                (self.grab,self.frame)=self.stream.read()
            
    def read(self):
        # most recent frame
        return self.frame
    
    def stop(self):
        # thread should be stopped now
        self.stopped = True

