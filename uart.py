import serial
from time import sleep

ser = serial.Serial("/dev/ttyTHS1")
ser.buadrate=115200
#9600
try:
    while True:
        dataToSend = "hi"
        ser.write(dataToSend.encode())
        #ser.write(dataToSend.encode())
        sleep(0.1)
        print("sent")

except KeyboardInterrupt:
    print("\nExiting Program")

ser.close()

