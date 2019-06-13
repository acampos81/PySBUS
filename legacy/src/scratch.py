from serial import Serial

ser = Serial('/dev/ttyS0')
ser.baudrate = 100000


def parse():
	while ser.readable():
	    byte = ser.read(1)
	    print(hex(byte[0]))

parse()


'''
    def parse(self):
        # reset the parser state if too much time has elapsed
        self.calculate_sbus_time()
        if self._sbus_time > SBUSConsts.SBUS_TIMEOUT_MS:
            self._parse_state = 0
            
        header = SBUSConsts.SBUS_HEADER[0]
        mask = SBUSConsts.SBUS2_MASK[0]
        footer = SBUSConsts.SBUS_FOOTER[0]
        footer2 = SBUSConsts.SBUS2_FOOTER[0]

        # see if serial data is available
        while self._ser.readable():
            self._sbus_time = 0
            self._cur_byte = self._ser.read(1)

            cur_byte = self._cur_byte[0]
            prev_byte = self._prev_byte[0]
            
            # find the header
            if self._parse_state == 0:
                if (cur_byte == header and prev_byte == footer) or ((prev_byte & mask) == footer2):
                    self._parse_state += 1
                else:
                    self._parse_state = 0
            else:
                # strip off the data
                if (self._parse_state-1) < SBUSConsts.PAYLOAD_SIZE:
                    self._payload[self._parse_state-1] = cur_byte
                    self._parse_state += 1

                # check the end byte
                if (self._parse_state-1) == SBUSConsts.PAYLOAD_SIZE:
                    for i in range(24):
                        print(i, hex(self._payload[i]))
                    if (cur_byte == footer) or ((cur_byte & mask) == footer2):
                        self._parse_state = 0
                        print("===================TRUE")
                        return True
                    else:
                        self._parse_state = 0
                        print("===================FALSE")
                        return False

            self._prev_byte = self._cur_byte
        
        # return false if partial packet
        return False
'''
