from gpiozero import Motor
from time import sleep
import socket
import json


# Server commands
HOST = '10.0.0.168'
HPORT = 65432
MSGLEN = 200

# Motor Ports
fRight = 17
bRight = 18
fLeft = 22
bLeft = 23
rMotor = Motor(fRight, bRight)
lMotor = Motor(fLeft, bLeft)


def commandMotor(command, motorNum):
    if motorNum == 0:
        motor = lMotor
    elif motorNum == 1:
        motor = lMotor

    if command[0] == 'f':
        speed = float(command[1:6])
        motor.forward(speed)
    elif command[0] == 'b':
        speed = float(command[1:6])
        motor.backward(speed)
    elif command[0] == 's':
        motor.stop()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, HPORT))
    while True:
        data = s.recv(MSGLEN).decode("utf-8")
        if data[0] == 'e':
            rMotor.stop()
            lMotor.stop()
            break
        rcomm = data[0:6]
        lcomm = data[6:12]
        print(rcomm + " " + lcomm)
        commandMotor(rcomm, 0)
        commandMotor(lcomm, 0)
        sleep(0.1)
