import sys
sys.path.append('/home/pi/raspberry-pi')
from pysbus.serial_parser import SerialParser

tty = sys.argv[1]
baud = int(sys.argv[2])
parser = SerialParser(tty, baud)
parser.begin()

try:
    while True:
        byte = parser.parse_raw()
        print(byte)
finally:
    parser.close()






