import serial

ser = serial.Serial('/dev/ttyTHS1',125000)

try:
    while True:
        data = [1,2,3,4,5,6,7,8]
        byte_data = bytearray(byte_data)
        ser.write(byte_data)
except:
    print("Exittiiinnnng")
finally:
    ser.close()
