import serial
from time import sleep

ser = serial.Serial(
        port="/dev/ttyTHS1",
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE
        )

try:
    while True:
        dataToSend = [1,2,3,4,5,6,7,8]
        dataToSend = bytearray(dataToSend)
        ser.write(dataToSend)

finally:
    ser.close()
