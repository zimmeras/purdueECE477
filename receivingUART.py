import serial 

port = "/dev/ttyTHS1"
rate = 115200

ser = serial.Serial(
        port="/dev/ttyTHS1",
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE)


try:
    while True:
        rec = ser.read(100)
        print("received:", rec)
except:
    print("uart communication interupted")
finally:
    ser.close()
