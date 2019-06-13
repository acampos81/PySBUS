import sys
sys.path.append('/home/pi/raspberry-pi')
from pysbus.softserial_parser import SoftSerialParser

rx = int(sys.argv[1])
baud = int(sys.argv[2])
parser = SoftSerialParser(rx, baud)
parser.begin()

try:
    while True:
        count, data = parser.parse_raw()
        if count > 0:
            print(data)
            #hex_string = "{0} [".format(baud)
            for i in range(count):
                print(i,data[i])
                #hex_string += "{0:#0{1}x}".format(data[i], 4)
                #if i < count-1:
                    #hex_string += ", "
            #hex_string += "]"
            #print(hex_string)
finally:
    parser.close()






