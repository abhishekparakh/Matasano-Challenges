#Implement AES CBC mode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
from Cryptodome.Util import Padding
import math
import P15


def unpadder(text, blockSizeInBits):    #text must be in bytes
    try:
        unpadded_data = Padding.unpad(text, blockSizeInBits/8, style='pkcs7')
    except ValueError:
        return 'PKCS#7 padding is incorrect.'
    #unpad = padding.PKCS7(blockSizeInBits).unpadder()
    #unpadded_data = unpad.update(text) + unpad.finalize()
    return unpadded_data                  #returns bytes


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
    xorOut = b''
    for s, t in zip(a,b):
        xorOut += bytes([s^t])    #^ works for bytes
    return xorOut      #returns bytes


def aesCBCMode(text, aesKey, IV, flag):    #incoming text must be bytes
    previousBlock = IV                      #first IV is all 0s
    if flag == 'd':
        pt = b''
        for i in range(0, len(text), 16):    #incoming text must be bytes
            currentBlock = text[i:i+16]         #take out 16 bytes
            currentDecrypt = aesECBMode(currentBlock, aesKey, flag)   #decrypt 16 bytes
            xoredBlock = xorInputs(currentDecrypt, previousBlock)    #xor with previous block
            pt += xoredBlock                    #the xored output is already a string
            previousBlock = currentBlock        #store current block for next round of CBC
        return pt                               #returns as bytes
    elif flag == 'e':
        text_padded = padder(text, 128)
        cipher = Cipher(algorithms.AES(aesKey), modes.CBC(IV), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(text_padded) + encryptor.finalize()  # convert ascii to bytes using .encode()
        return ct                          #returns bytes
    else:
        return "Invalid Flag! It can be e for encryption or d for decryption only."


def main():
    f = open('10altEnc.txt', 'r')       #open input file - assuming it is base64 encoded
    ct = f.read()                 #read the file
    f.close()
    ct = base64.b64decode(ct)     #decode base64 - ct is now in bytes
    aesKey = b'NO PAIN NO GAIN!'     #input key in bytes
    IV = b'\x00'*16                  #IV in bytes
    #ct = aesCBCMode(pt.encode(), aesKey, IV, 'e')
    #b64CT = base64.b64encode(ct)
    #f1 = open('10altEnc.txt', 'w')
    #f1.write(str(b64CT, 'latin1'))
    #f1.close()
    pt = aesCBCMode(ct, aesKey, IV, 'd')    #Call CBC mode with flag of d
    unpaddedPT = str(unpadder(pt, 128), 'latin1')
    print(unpaddedPT)





if __name__ == "__main__":
    main()