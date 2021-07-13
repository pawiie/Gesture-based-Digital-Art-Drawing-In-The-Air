"""
Created on Thu Apr 20 2021 15:44:36

@author: PS Chauhan
"""


from flask import Flask, render_template, Response
import cv2,socket ,json, time

app = Flask(__name__)

# root => index page
@app.route('/')
def hello():
    return render_template('index.html')

# function to get the coordinates
def getCoordinates():
    # trigger the server(object tracking) when this function is called
    #use async and wait 
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hostIP = '127.0.0.1'
    port = 9999
    clientSocket.connect((hostIP,port))

    while True:
        packet = clientSocket.recv(14)
        # print(packet.decode())
        data = packet.decode()
        if not data == 'null':
            yield "data:"+str(data)+"\n\n"

        # automate the break and also in the server
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    clientSocket.close()


# def pawan_d():
    # # return "pawan"
    # i=1
    # while(1):
    #     # print(i)
    #     time.sleep(0.02)
    #     yield 'data: '+str(i)+'\n\n'
    
# route to get the streams of coordinates
@app.route('/coordinates')
def coordinates():
    return Response(getCoordinates(),mimetype="text/event-stream")

# @app.route('/pawan')
# def pawan():
#     return Response(pawan_d(),mimetype="text/event-stream")
    




