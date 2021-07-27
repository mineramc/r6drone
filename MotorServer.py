import socket
from socket import timeout
from time import sleep
import pygame

HOST = ''
PORT = 65432
MSGLEN = 100

pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joystickEnabled = joysticks.len > 0

def joystickToInput():
    command = ""
    pygame.event.pump()
    joystick = joysticks[0]
    joystick.init()
    leftVal = clearThreshold(joystick.get_axis(1))
    rightVal = clearThreshold(joystick.get_axis(3))

    print("Axis 1: " + str(leftVal))
    print("Axis 3: " + str(rightVal))
    return ""

def clearThreshold(joystickVal):
    if joystickVal < 0.0001:
        return 0
    else:
        return joystickVal

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print('Connected by', addr)
    with conn:
        inputCommand = ''
        while inputCommand != "end":
            if joystickEnabled:
                inputCommand = joystickToInput()
            else:
                inputCommand = input()
            print(inputCommand)
            conn.sendall(inputCommand.encode())


