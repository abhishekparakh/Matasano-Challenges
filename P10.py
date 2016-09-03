#Implement AES CBC mode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import math

def padder(text, blockSizeInBits):     #padder just returns a text stream padded with bits
    padder = padding.PKCS7(blockSizeInBits).padder()
    padded_data = padder.update(text) + padder.finalize()
    return padded_data

#This AES ECB mode function does both encryption and decryption
def aesECBMode(text, aesKey, flag):    #flag tells the function to enc or dec
    if type(text) == str:
        text = text.encode()
    cipher = Cipher(algorithms.AES(aesKey), modes.ECB(), backend=default_backend())

    if flag == 'd':       #decrypt: the incoming text must be in bytes
        ct = text
        decryptor = cipher.decryptor()
        textOut = decryptor.update(ct) + decryptor.finalize()  # output is in bytes
        return textOut      #this returns bytes
    elif flag == 'e':     #encrypt: the incoming text in bytes
        text = padder(text, 128)    #AES block size is fixed to 128 bits
        encryptor = cipher.encryptor()
        ct = encryptor.update(text) + encryptor.finalize()    #convert ascii to bytes using .encode()
        return ct          #returns bytes
    else:
        return 'Invalid Flag'


def xorInputs(a, b):    #works for bytes and ints
    xorOut = ''
    for s, t in zip(a,b):
        xorOut += chr(s ^ t)   #^ works for bytes
    return xorOut      #returns a string


def aesCBCMode(text, aesKey, IV, flag):      #this function calls ECB mode inside
    previousBlock = IV                      #first IV is all 0s
    if flag == 'd':
        pt = ''
        for i in range(0, len(text), 16):    #incoming text must be bytes
            currentBlock = text[i:i+16]         #take out 16 bytes
            currentDecrypt = aesECBMode(currentBlock, aesKey, flag)   #decrypt 16 bytes
            xoredBlock = xorInputs(currentDecrypt, previousBlock)    #xor with previous block
            pt += xoredBlock                    #the xored output is already a string
            previousBlock = currentBlock        #store current block for next round of CBC
        return pt                               #returns a string
    elif flag == 'e':
        text_padded = padder(text, 128)
        cipher = Cipher(algorithms.AES(aesKey), modes.CBC(IV), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(text_padded) + encryptor.finalize()  # convert ascii to bytes using .encode()
        return ct                          #returns bytes
    else:
        return "Invalid Flag! It can be e for encryption or d for decryption only."


def main():
    f = open('10.txt', 'r')       #open input file - assuming it is base64 encoded
    ct = f.read()                 #read the file
    f.close()
    ct = base64.b64decode(ct)     #decode base64 - ct is now in bytes
    aesKey = b'YELLOW SUBMARINE'     #input key in bytes
    IV = b'\x00'*16                  #IV in bytes
    ct = aesCBCMode('Yellow SubmarineYellow Submarin'.encode(), aesKey, IV, 'e')
    print(aesCBCMode(ct, aesKey, IV, 'd'))    #Call CBC mode with flag of d



if __name__ == "__main__":
    main()