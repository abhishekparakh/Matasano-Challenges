#Set 1, Challenge 2

import binascii
from bitstring import BitArray

def strXOR(a, b):
    return BitArray(binascii.unhexlify(a))^BitArray(binascii.unhexlify(b))


def main():
    a = '1c0111001f010100061a024b53535009181c'
    b = '686974207468652062756c6c277320657965'
    print(strXOR(a, b))

if __name__ == '__main__':
    main()