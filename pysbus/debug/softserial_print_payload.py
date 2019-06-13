import sys
sys.path.append('/home/pi/raspberry-pi')
from pysbus.softserial_parser import SoftSerialParser
from pysbus.constants import SBUSConsts

rx = int(sys.argv[1])
baud = int(sys.argv[2])
parser = SoftSerialParser(rx, baud)
payload = [0] * SBUSConsts.PAYLOAD_SIZE

parser.begin()

try:
    while True:
        success = parser.parse(payload)
        length = SBUSConsts.PAYLOAD_SIZE
        hex_string = "["
        for i in range(length):
            hex_string += "{0:#0{1}x}".format(payload[i], 4)
            if i < length-1:
                hex_string += ", "
        hex_string += "] {0}".format(success)
        print(hex_string)
except:
    parser.close()
    sys.exit(1)
    raise()
