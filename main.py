# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import socket
import numpy as np
from PIL import Image
from _pickle import dumps, loads
from socket import timeout
import cv2


HOST = ''  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
frameSize = (1920, 1080)
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 60, frameSize)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    data = []
    full_data = b""
    counter = 0
    with conn:
        conn.settimeout(0.1)
        print('Connected by', addr)
        while True:
            counter += 1
            print("waiting" + str(counter))
            try:
                packet = conn.recv(4096)
            except timeout:
                break
            data.append(packet)
            print("append" + str(counter))
    array = loads(full_data)
    img = Image.fromarray(array, 'RGB')
    img.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
