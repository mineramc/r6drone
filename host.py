import cv2
import io
import socket
from PIL import Image


HOST = ''
PORT = 65432

test = len('asdfasdf').to_bytes(16, 'big')
print(len(test))
print(int.from_bytes(test[:16], 'big'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    connection, address = s.accept()
    print(f'Accepted client at {address[0]}')

    with connection:
        data = bytearray()
        missing_bytes = 0
        while True:
            packet = connection.recv(4096)
            if packet:
                if missing_bytes == 0:
                    # TODO: show image here
                    print('showed image')

                    len_data = packet[:16]
                    missing_bytes = int.from_bytes(len_data, 'big')
                    packet = packet[16:]
                print(missing_bytes)
                chunk = packet[:missing_bytes]
                data.extend(chunk)
                missing_bytes -= len(chunk)
