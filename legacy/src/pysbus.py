import time
from serial import Serial
from src.constants import SBUSConsts

class SBUS:
    def __init__(self, tty="/dev/ttyS0", baud=98000):
        self._ser = None
        self._tty = tty
        self._baud = baud
        self._parse_state = 0
        self._prev_byte = b'\x00'
        self._cur_byte = b'\x00'
        self._payload = [0] * SBUSConsts.PAYLOAD_SIZE
        self._sbus_min = [0] * SBUSConsts.NUM_CHANNELS
        self._sbus_max = [0] * SBUSConsts.NUM_CHANNELS
        self._sbus_scale = [0.0] * SBUSConsts.NUM_CHANNELS
        self._sbus_bias = [0.0] * SBUSConsts.NUM_CHANNELS
        self._read_len = [0] * SBUSConsts.NUM_CHANNELS
        self._write_len = [0] * SBUSConsts.NUM_CHANNELS
        self._use_read_coeff = [False] * SBUSConsts.NUM_CHANNELS
        self._use_write_coeff = [False] * SBUSConsts.NUM_CHANNELS
        self._read_coeff = 0.0
        self._write_coeff = 0.0
        self._sbus_time = 0
        self._current_milli_time = lambda: int(round(time.time() * 1000))
        self._last_milli_time = 0

    def begin(self):
        # initialize parse state
        self._parse_state = 0

        # initialize default scale factors and biases
        for i in range(SBUSConsts.NUM_CHANNELS):
            self.set_endpoints(i, SBUSConsts.DEFAULT_MIN, SBUSConsts.DEFAULT_MAX)

        # begin serial port for SBUS
        self._ser = Serial(self._tty)
        self._ser.baudrate = self._baud
        self._ser.timeout = 1

    def close(self):
        self._ser.flush()
        self._ser.close()

    def read(self, channels):
        payload_ready = self.parse()
        failsafe = False
        lost_frame = False

        if payload_ready:
            if channels is not None:
                payload = self._payload
                channels[0]  = (payload[1]        | payload[2]  << 8) & 0x07FF
                channels[1]  = (payload[2]  >> 3  | payload[3]  << 5) & 0x07FF
                channels[2]  = (payload[3]  >> 6  | payload[4]  << 2  | payload[5] << 10) & 0x07FF
                channels[3]  = (payload[5]  >> 1  | payload[6]  << 7) & 0x07FF
                channels[4]  = (payload[6]  >> 4  | payload[7]  << 4) & 0x07FF
                channels[5]  = (payload[7]  >> 7  | payload[8]  << 1  | payload[9] << 9) & 0x07FF
                channels[6]  = (payload[9]  >> 2  | payload[10] << 6) & 0x07FF
                channels[7]  = (payload[10] >> 5  | payload[11] << 3) & 0x07FF
                channels[8]  = (payload[12]       | payload[13] << 8) & 0x07FF
                channels[9]  = (payload[13] >> 3  | payload[14] << 5) & 0x07FF
                channels[10] = (payload[14] >> 6  | payload[15] << 2  | payload[16] << 10) & 0x07FF
                channels[11] = (payload[16] >> 1  | payload[17] << 7) & 0x07FF
                channels[12] = (payload[17] >> 4  | payload[18] << 4) & 0x07FF
                channels[13] = (payload[18] >> 7  | payload[19] << 1  | payload[20] << 9) & 0x07FF
                channels[14] = (payload[20] >> 2  | payload[21] << 6) & 0x07FF
                channels[15] = (payload[21] >> 5  | payload[22] << 3) & 0x07FF

                lost_frame = (payload[23] & SBUSConsts.SBUS_LOST_FRAME[0]) > 0
                failsafe = (payload[23] & SBUSConsts.SBUS_FAILSAFE[0]) > 0
        
        return payload_ready, failsafe, lost_frame

    def write(self, channels):
        pass

    def read_cal(self, cal_channels, failsafe, lost_frame):
        pass

    def write_cal(self, channels):
        pass

    def set_endpoints(self, channel, ch_min, ch_max):
        self._sbus_min[channel] = ch_min
        self._sbus_max[channel] = ch_max
        self.scale_bias(channel)

    def get_endpoints(self, channel):
        ch_min = _sbus_min[channel]
        ch_max = _sbus_max[channel]
        return ch_min, ch_max

    def set_read_cal(self, channel, coeff, length):
        pass

    def get_read_cal(self, channel, coeff, length):
        pass

    def set_write_cal(self, channel, coeff, length):
        pass

    def get_write_cal(self, channel, coeff, length):
        pass

    def calculate_sbus_time(self):
        # initialize _last_milli_time in order to get a delta
        if self._last_milli_time == 0:
            self._last_milli_time = self._current_milli_time()
            return

        self._sbus_time = self._current_milli_time() - self._last_milli_time
        self._last_milli_time = self._current_milli_time()
    
    def parse(self):
        header = SBUSConsts.SBUS_HEADER[0]
        footer = SBUSConsts.SBUS_FOOTER[0]
        self._cur_byte = b'\x00'
        self._prev_byte = b'\x00'

        # see if serial data is available
        while self._ser.readable():
            self._cur_byte = self._ser.read(1)
            
            if len(self._cur_byte) == 0:
                break
            
            cur_byte = self._cur_byte[0]
            prev_byte = self._prev_byte[0]
            
            # find the header
            if self._parse_state == 0:
                if cur_byte == header and prev_byte == footer:
                    self._payload[self._parse_state] = cur_byte
                    self._parse_state += 1
                else:
                    self._parse_state = 0
            else:
                # strip off the data
                if self._parse_state < SBUSConsts.PAYLOAD_SIZE:
                    self._payload[self._parse_state] = cur_byte
                    self._parse_state += 1

                # check the end byte
                if self._parse_state == SBUSConsts.PAYLOAD_SIZE:
                    if cur_byte == footer:
                        self._parse_state = 0
                        return True
                    else:
                        self._parse_state = 0
                        return False

            self._prev_byte = self._cur_byte
        
        # return false if partial packet
        return False
    
    
    def scale_bias(self, channel):
        ch_min = self._sbus_min[channel]
        ch_max = self._sbus_max[channel]
        self._sbus_scale[channel] = 2.0 / (ch_max - ch_min)
        self._sbus_bias[channel] = -1.0 * (ch_min + (ch_max - ch_min) / 2.0) * self._sbus_scale[channel]

    
    def poly_val(self, poly_size, coefficients, x):
        pass


