import sys
sys.path.append('/home/pi/raspberry-pi')
from pysbus.sbus import SBUS
from pysbus.softserial_parser import SoftSerialParser
from pysbus.constants import SBUSConsts

rx = int(sys.argv[1])
baud = int(sys.argv[2])
sbus = SBUS(
    SoftSerialParser(rx, baud)
)

channels = [0] * SBUSConsts.NUM_CHANNELS

sbus.begin()

try:
    while True:
        payload_ready, failsafe, lost_frame = sbus.read(channels)
        if payload_ready:
            print(channels,"Payload: {0} | Failsafe: {1} | Lost Frame: {2}".format(payload_ready,failsafe,lost_frame))
finally:
    sbus.close()
    sys.exit(1)

