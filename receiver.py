import socket
import cv2
from _pickle import dumps, loads

HOST = '10.0.0.168'     # The server's hostname or IP address
PORT = 65432            # The port used by the server

image = cv2.imread('tenki_no_ko.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

video = cv2.VideoCapture('sparkle.mp4')

data = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while video.isOpened():
        ret, frame = video.read()
        s.sendall(dumps(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        s.send(42069)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    video.release()
    cv2.destroyAllWindows()
    print('finished sending')

    while True:
        print('looping')
        packet = s.recv(4096)     # Waits infinitely until a packet is received
        if not packet:
            break
        data.append(packet)

cv2.imshow('tenki_no_ko', cv2.cvtColor(loads(b"".join(data)), cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
