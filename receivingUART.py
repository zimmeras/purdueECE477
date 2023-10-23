import serial 

port = "/dev/ttyTHS1"
rate = 115200

ser = serial.Serial(port, rate)

try:
    while True:
        rec = ser.read(100)
        print("received:", rec)
except:
    print("uart communication interupted")
finally:
    ser.close()