import sys
from serial import Serial


tty = sys.argv[1]
ser = Serial(tty)
ser.flush()
ser.close() 
