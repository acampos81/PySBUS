from serial import Serial

ser = Serial("/dev/ttyS0")
ser.baudrate = 100000

while True:
    print(ser.read(1))
