import struct
import cv2,socket ,json

def liveData():
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hostIP = '127.0.0.1'
    port = 9999
    clientSocket.connect((hostIP,port))
    # data = b""
    # payloadSize = struct.calcsize("Q")

    while True:
        packet = clientSocket.recv(14)
        # print(packet.decode())
        data = packet.decode()
        if not data == 'null':
            yield data
        

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
    clientSocket.close()

for i in liveData():
    print(i)