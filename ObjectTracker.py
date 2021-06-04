"""
Created on Wed Apr 2021 12 22:35:33 

@author: PS Chauhan
"""

"""
It is the main file for tracking the object and
finding the coordinates of the movements
"""

# import the necessary packages


# creating object of the log class in logger
from collections import deque
from imutils.video import VideoStream
import cv2
import imutils
import time
import ColourFinder
import logger
import fps
import socket
import json,pickle,struct
OT_log = logger.Log()


# getting the HSV range of colour of the object

# CF = ColourFinder.ColourFinder()
# LowerHSV,UpperHSV = CF.HSVRange()


# yellowish  green colour
#LowerHSV =(29, 86, 6)
#UpperHSV =(64, 255, 255)

# for red
#LowerHSV =(0, 70, 50)
#UpperHSV =(10, 255, 255)

# green
LowerHSV = (20, 80, 100)
UpperHSV = (50, 255, 255)


# currently not using any multi threading
vs = VideoStream(src=0).start()

# allow the camera or video file to warm up i.e., for camera to open and adjust
time.sleep(2.0)

# double ended queue to store the coordinates (insert and pop operation takes O(1) )
pts = deque()

# object of fps class
_fps = fps.FPS()

# starting the fps counter
_fps.start()


# create socket
try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('hello')
    print(serverSocket)
except:
    print("could not create server socket")
    OT_log.addLog('error', "could not create the sever socket")
    exit

try:
    hostName = socket.gethostname()
    hostIP = socket.gethostbyname(hostName)

    # for live debugging
    print('hostIP: ', hostIP)
    # OT_log.addLog('warning','hostIP: '+hostIP)
except:
    OT_log.addLog('error', 'could not get hostname')
    exit

# port for listening
port = 9999

socketAddress = (hostIP, port)

# socket bind
try:
    serverSocket.bind(socketAddress)
except:
    OT_log.addLog('error', 'could not bind the sever socket address')
    exit


# socket listen

serverSocket.listen(5)  # 5 is back log int

print('listening at : ', socketAddress)
# OT_log.addLog('listening at : '+socketAddress)

clientSocket, addr = serverSocket.accept()
# loop till we get the feed from camera
while True:
    # clientSocket, addr = serverSocket.accept()
    # socket accept
    # try:

    #     # OT_log.addLog('accepting the request from  : '+addr)
    # except:
    #     print(clientSocket,addr)
    #     OT_log.addLog('error','Could accept the request from client')

    # if could not get connection
    if clientSocket:
        frame = vs.read()

        # update the fps
        _fps.update()

        # to counter the mirror effect
        frame = cv2.flip(frame, 1)

        # if no frame is detected
        if frame is None:
            OT_log.addLog('error', 'no frames detected')
            break

        # resize the frame, blur it, and convert it to the HSV color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color selected, then perform
        # a series of dilations and erosions to remove any small blobs left in the mask

        mask = cv2.inRange(hsv, LowerHSV, UpperHSV)

        # for red
        #mask = cv2.inRange(hsv, (170, 70, 50), (180, 255, 255))
        #
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball

        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
            # # 	# draw the circle and centroid on the frame,
            # # 	# then update the list of tracked points
            #      cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            #      cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # # update the points queue
        print(center)
        # a = pickle.dumps(center)
        # message = struct.pack("Q",len(a))+a
        # #print(message)
        # clientSocket.sendall(message)
        # pts.append(center)

        data = json.dumps(center).encode()
        clientSocket.sendall(data)

        # print('data :', data)

        # print('decode data: ', json.loads(data))

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
    # while len(pts)>1:
    #     a=pts.popleft()
    #     b=pts[0]
    #     if a is None or b is None:
    #         continue
    #     print("pts: ", a, b)
    #     thickness = int(5)
    #     cv2.line(frame, b, a, (0, 0, 255), thickness)
    # cv2.imshow("Frame", frame)


# STOPING THE CAMERA FEED

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    # change this according to the UI of the drawing board
    if key == ord("q"):

        # stop the camera video stream thread
        vs.stop()
        OT_log.addLog('warning', 'closing the camera feed')

        # clsong the socket connection
        clientSocket.close()
        serverSocket.close()
        OT_log.addLog("closed  the server socket")
        break


# stop the fps counter
_fps.end()

# output fps achieved
print("FPS achieved: ", _fps.fps())


# close all windows
cv2.destroyAllWindows()
