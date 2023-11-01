import serial 

serial_port = serial.Serial(
        port="/dev/ttyTHS1",
        buadrate=125000,
        timeout=1
        )


try:
    while True:

        data = serial_port.readline()
        decoded_data = data.decode("utf-8")
        print(decode_data, end="")

except:
    print("Exitttinnng")
finally:
    serial_port.close()


