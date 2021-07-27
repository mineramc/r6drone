from gpiozero import Motor
from time import sleep
import socket


# Server commands
HOST = '10.0.0.168'
HPORT = 65432
MSGLEN = 100

# Motor Ports
fRight = 17
bRight = 18
fLeft = 22
bLeft = 23
rMotor = Motor(fRight, bRight)

receivedMessage = ""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, HPORT))
    while receivedMessage != "e":
        data = s.recv(MSGLEN)
        receivedMessage = data.decode("utf-8")
        command = receivedMessage[0]
        print(command)
        if command == 'f':
            speed = float(receivedMessage[1:6])
            rMotor.forward(speed)
        elif command == 'b':
            speed = float(receivedMessage[1:6])
            rMotor.backward(speed)
        elif command == 's':
            rMotor.stop()
        elif command == 'e':
            rMotor.stop()
            break
        else:
            continue
        sleep(0.1)
