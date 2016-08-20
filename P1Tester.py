# This program is a tester for P11.py that converts a hex string to b64

import P11 as myB64
import binascii
import re

#hexInput = "0x49 0x27   0x6d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

def main():
    f = open('hexInput.txt', 'r')

    for ln in f:
        # using regular expressions to strip white spaces from in between
        hexInput = re.sub('[\s+]', '', ln).replace('0x', '').strip()

        b64 = binascii.b2a_base64(binascii.unhexlify(hexInput)).decode('ascii').strip()
        myOutput = myB64.b64Convert(hexInput).strip()

        print(myOutput == b64)


if __name__ == '__main__':
    main()