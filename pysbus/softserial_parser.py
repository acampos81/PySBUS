import time
import pigpio
from .constants import SBUSConsts


class SoftSerialParser:
    def __init__(self, rx, baud, bits=8, timeout_ms=1000):
        self._pi = pigpio.pi()
        self._rx = rx
        self._bits = bits
        self._baud = baud
        self._parse_state = 0
        self._prev_byte = 0
        self._cur_byte = 0
        self._timeout = timeout_ms/1000
        self._elapsed_ms = 0
        self._last_ms = 0
    
    def begin(self):
        self._parse_state = 0
        self._pi.set_mode(self._rx, pigpio.INPUT)

        # fatal exceptions off (so that closing an unopened gpio doesn't error)
        pigpio.exceptions = False
        self._pi.bb_serial_read_close(self._rx)
    
        # fatal exceptions on
        pigpio.exceptions = True

        # open a gpio to bit bang read data
        self._pi.bb_serial_read_open(self._rx, self._baud, self._bits)

    def close(self):
        self._pi.bb_serial_read_close(self._rx)
        self._pi.stop()
        
    def _check_timeout(self):
        current_ms = time.time()
        
        if self._last_ms == 0:
            self._last_ms = current_ms

        self._elapsed_ms += current_ms - self._last_ms
        self._last_ms = current_ms
        
        return self._elapsed_ms > self._timeout

    def parse_raw(self):
        return self._pi.bb_serial_read(self._rx)
    
    def parse(self, payload):
        header = SBUSConsts.SBUS_HEADER[0]
        footer = SBUSConsts.SBUS_FOOTER[0]
        self._cur_byte = 0
        self._prev_byte = 0
        
        while True:
            (count, data) = self._pi.bb_serial_read(self._rx)
            
            # keep track of duration of emtpy data to prevent infinite loop
            if count == 0:
                if self._check_timeout():
                    break
                else:
                    continue
            else:
                self._elapsed_ms = 0
            
            # see if serial data is available
            for i in range (len(data)):
                self._cur_byte = data[i]
        
                # find the header
                if self._parse_state == 0:
                    if self._cur_byte == header and self._prev_byte == footer:
                        payload[self._parse_state] = self._cur_byte
                        self._parse_state += 1
                    else:
                        self._parse_state = 0
                else:
                    # strip off the data
                    if self._parse_state < 25:
                        payload[self._parse_state] = self._cur_byte
                        self._parse_state += 1
        
                    # check the end byte
                    if self._parse_state == 25:
                        if self._cur_byte == footer:
                            self._parse_state = 0
                            return True
                        else:
                            self._parse_state = 0
                            return False
        
                self._prev_byte = self._cur_byte
