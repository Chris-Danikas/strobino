from socket import timeout
import serial
import time
import sys

arduinoUNO = serial.Serial(port="COM3", baudrate=9600, timeout=0.1)
# gia write p.x. 50: pin 5, LOW


def write_read(x):
    arduinoUNO.write(bytes(x, 'utf-8'))

def beat(x):
    arduinoUNO.write(bytes(x + '1', 'utf-8'))
    time.sleep(0.1)
    arduinoUNO.write(bytes(x + '0', 'utf-8'))