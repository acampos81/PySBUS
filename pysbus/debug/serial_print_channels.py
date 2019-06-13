import sys
sys.path.append('/home/pi/raspberry-pi')
from pysbus.sbus import SBUS
from pysbus.serial_parser import SerialParser
from pysbus.constants import SBUSConsts

tty = sys.argv[1]
baud = sys.argv[2]
sbus = SBUS(
    SerialParser(tty, baud)
)

channels = [0] * SBUSConsts.NUM_CHANNELS

sbus.begin()

try:
    while True:
        payload_ready, failsafe, lost_frame = sbus.read(channels)
        print(channels,"Payload: {0} | Failsafe: {1} | Lost Frame: {2}".format(payload_ready,failsafe,lost_frame))
finally:
    sbus.close()
    sys.exit(1)

