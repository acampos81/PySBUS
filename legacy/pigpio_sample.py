import sys
import pigpio

TX = 23
RX = 24

if len(sys.argv) > 1:
    baud = int(sys.argv[1])
else:
    baud = 115200

if len(sys.argv) > 2:
    bits = int(sys.argv[2])
else:
    bits = 8

pi = pigpio.pi()

pi.set_mode(RX, pigpio.INPUT)
pi.set_mode(TX, pigpio.OUTPUT)

# fatal exceptions off (so that closing an unopened gpio doesn't error)

pigpio.exceptions = False

pi.bb_serial_read_close(RX)

# fatal exceptions on

pigpio.exceptions = True


# open a gpio to bit bang read the echoed data
pi.bb_serial_read_open(RX, baud, bits)

__payload = [0] * 25
__parse_state = 0


def parse(data):
    global __parse_state
    global __payload
    header = 0x0F
    footer = 0x00
    __cur_byte = 0
    __prev_byte = 0

    # see if serial data is available
    for i in range (len(data)):
        __cur_byte = data[i]
        cur_byte = __cur_byte
        prev_byte = __prev_byte

        # find the header
        if __parse_state == 0:
            if cur_byte == header and prev_byte == footer:
                __payload[__parse_state] = cur_byte
                __parse_state += 1
            else:
                __parse_state = 0
        else:
            # strip off the data
            if __parse_state < 25:
                __payload[__parse_state] = cur_byte
                __parse_state += 1

            # check the end byte
            if __parse_state == 25:
                if cur_byte == footer:
                    __parse_state = 0
                    return True
                else:
                    __parse_state = 0
                    return False

        __prev_byte = __cur_byte

    return False


try:
    while True:
        (count, data) = pi.bb_serial_read(RX)
        if count > 0:
            if parse(data):
                hex_string = "["
                length = len(__payload)
                for i in range(length):
                    hex_string += "{0:#0{1}x}".format(__payload[i],4)
                    if i < length-1:
                        hex_string += ", "
                hex_string += "]"
                print(hex_string)

except:
    pi.bb_serial_read_close(RX)
    pi.stop()
    raise()
