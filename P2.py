#Set 1, Challenge 2

import binascii
from bitstring import BitArray

def strXOR(a, b):
    return BitArray(binascii.unhexlify(a))^BitArray(binascii.unhexlify(b))


def main():
    a = '9c863d374184079d60066b3b4a193d3354c7'
    b = '2ca09c99b91d85d444e7c3a8beadeeff4f1c'
    print(strXOR(a, b).hex)

if __name__ == '__main__':
    main()