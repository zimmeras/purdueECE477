import serial
from time import sleep

ser = serial.Serial(port="/dev/ttyTHS1", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        

try:
    
    dataToSend = bytearray([62, 63, 64, 66, 55, 66, 88, 98])
    ser.write(dataToSend)
    print(dataToSend)
    #data = "hii"
    #ser.write(data.encode('ascii'))
        #sleep(1)
    

        #recv = ser.read(50)
        #if recv:
        #    print("received data from stm32:", recv.decode())

except KeyboardInterrupt:
    print("\nExiting Program")

ser.close()
