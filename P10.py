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
    cipher = Cipher(algorithms.AES(aesKey), modes.ECB(), backend=default_backend())

    if flag == 'd':       #decrypt: the incoming text must be in bytes
        ct = text
        decryptor = cipher.decryptor()
        textOut = decryptor.update(ct) + decryptor.finalize()  # output is in bytes
        return textOut      #this returns bytes
    elif flag == 'e':     #encrypt: the incoming text can be in ascii (english stream)
        msg = text
        padded_data = padder(msg, 128)    #AES block size is fixed to 128 bits
        encryptor = cipher.encryptor()
        ct = encryptor.update(msg.encode()) + encryptor.finalize()    #convert ascii to bytes using .encode()
        return ct          #returns bytes
    else:
        return 'Invalid Flag'

def xorInputs(a, b):    #works for bytes and ints
    xorOut = ''
    for s, t in zip(a,b):
        xorOut += chr(s ^ t)   #^ works for bytes
    return xorOut      #returns a string

def aesCBCMode(text, aesKey, IV, flag):      #this function calls ECB mode inside
    ct = ''
    padded_data = padder(text, 128)         #pad input to AES block length
    #print(padded_data)
    #print(len(padded_data))
    previousBlock = IV                      #first IV is all 0s
    for i in range(0, len(text)//16, 16):   #16 byte blocks
        currentBlock = text[i:i+16]         #take out 16 bytes
        #print(currentBlock)
        #print(previousBlock)
        currentDecrypt = aesECBMode(currentBlock, aesKey, flag)   #decrypt 16 bytes
        xoredBlock = xorInputs(currentDecrypt, previousBlock)    #xor with previous block
        #print(xoredBlock)
        ct += xoredBlock                    #the xored output is already a string
        previousBlock = currentBlock        #store current block for next round of CBC
    return ct

def main():
    f = open('10.txt', 'r')       #open input file - assuming it is base64 encoded
    ct = f.read()                 #read the file
    ct = base64.b64decode(ct)     #decode base64 - ct is now in bytes
    #print(ct)
    aesKey = b'YELLOW SUBMARINE'     #input key in bytes
    IV = b'\x00'*16                  #IV in bytes
    #print(type(IV))
    print(aesCBCMode(ct, aesKey, IV, 'd'))    #Call CBC mode with flag of d



if __name__ == "__main__":
    main()