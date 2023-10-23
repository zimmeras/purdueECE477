import serial
from time import sleep

ser = serial.Serial("/dev/ttyTHS1", timeout=1)
ser.buadrate=115200
#9600
try:
    while True:
        dataToSend = "Hello,Jetson Here !\n"
        ser.write(dataToSend.encode())
        sleep(1)
    
    
    #while True:

     #   recv = ser.read(50)
      #  if recv:
      #      print("received data from stm32:", recv.decode(), end="")
      #      break
except KeyboardInterrupt:
    print("\nExiting Program")

ser.close()
