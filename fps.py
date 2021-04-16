"""
Created on Thu Apr 15 2021 16:09:08

@author: PS Chauhan
"""

"""
This module is to find the frames per second of the VideoStream
utilised while reading and processing the frames
""" 

import datetime

class FPS:
    def __init__(self):
        self._start = None
        self._end = None
        self._numframes = 0
    
    def start(self):
        self._start = datetime.datetime.now()
        return self
    
    def end(self):
        self._end = datetime.datetime.now()
    
    def update(self):
        #update the total number of frames in the start and end interval

        self._numframes += 1

    def elapsed(self):
        #returns the time interval
        return(self._end - self._start).total_seconds()

    def fps(self):
        return self._numframes/self.elapsed()
     