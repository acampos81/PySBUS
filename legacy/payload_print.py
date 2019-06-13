import sys
import time
from src.pysbus import SBUS
from src.constants import SBUSConsts

tty = sys.argv[1]
baud = sys.argv[2]
sbus = SBUS(tty, baud)
channels = [0] * SBUSConsts.NUM_CHANNELS

sbus.begin()

try:
    while True:
        
        success = sbus.parse()
        length = len(sbus._payload)
        hex_string = "["
        for i in range(length):
            hex_string += "{0:#0{1}x}".format(sbus._payload[i],4)
            if i < length-1:
                hex_string += ", "
        hex_string += "] {0}".format(success)
        print(hex_string)
        
        
        
except KeyboardInterrupt:
    print("Closing serial port")
    sbus.close()
    sys.exit(1)
