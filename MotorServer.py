import socket
from socket import timeout
from time import sleep
import pygame
import json

HOST = ''
PORT = 65432
MSGLEN = 200

pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joystickEnabled = len(joysticks) > 0

def joystickToInput():
    pygame.event.pump()
    joystick = joysticks[0]
    joystick.init()
    stopButton = joystick.get_button(3)
    if stopButton == 1:
        return "ee"
    leftVal = clearThreshold(joystick.get_axis(1))
    rightVal = clearThreshold(joystick.get_axis(3))
    leftCommand = valueToString(leftVal)
    rightCommand = valueToString(rightVal)
    print("Right: " + str(rightVal))
    print("Left: " + str(leftVal))
    return rightCommand + leftCommand


def valueToString(joystickVal):
    if joystickVal == 0:
        return "s0.000"
    elif joystickVal > 0:
        if joystickVal == 1.0:
            return "b1.000"
        return "b" + str("{:.3f}".format(abs(joystickVal)))
    else:
        if joystickVal == -1.0:
            return "f1.000"
        return "f" + str("{:.3f}".format(abs(joystickVal)))


def clearThreshold(joystickVal):
    if abs(joystickVal) < 0.0001:
        return 0
    else:
        return round(joystickVal, 3)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print('Connected by', addr)
    with conn:
        inputCommand = ' '
        while inputCommand[0] != 'e':
            if joystickEnabled:
                inputCommand = joystickToInput()
            else:
                #todo: Graphical/CommandLine
                inputCommand = "ee"
            print(inputCommand)
            conn.sendall(inputCommand.encode())
            sleep(0.15)


