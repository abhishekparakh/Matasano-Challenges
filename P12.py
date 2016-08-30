#Byte-at-a-time ECB decryption
import P10, P11   #my implementation of AES CBC mode
import os
import base64


AESKeyLength = 16  # size in bytes
key = os.urandom(AESKeyLength)  # generate random key and fix it for this program
def AESECBOracle(data, unknownString, offset):
    dataInBytes = data.encode() + base64.b64decode(unknownString)[offset:]  #append the random string before encrypting
    encOut = P10.aesECBMode(dataInBytes, key,'e')   #reusing functions from P10
    return encOut          #returns bytes if encrypt (flag = e)


def discoverBlockSize(unknownString):
    flag = 0            #flag is set once block size is discovered
    blockSize = 1       #start with a block size of 1 byte, increments in 1 byte as well
    while flag == False:
        text = 'A' * blockSize
        encText = AESECBOracle(text, unknownString, offset=0)       #encText is in bytes
        flag = P11.AESDetectionOracle(encText)      #flag will be T or F
        if flag == False: blockSize += 1            #if ECB not found, increment block size
    return blockSize//2  #divide by 2-using AES detection to compute block size. Detection happens only at 2 blocks


def decryptUnknownStringByteAtATime(blockSize, unknownString):
    #craft a byte short input
    unknownStringDecrypted = ''
    for j in range(0, len(unknownString)):  #j chops off unknownString as it is decrypted
        i = 0
        byteDecrypted = False
        while byteDecrypted == False:
            firstBlock = 'A'*(blockSize-1) + chr(i)
            shortSecondBlock = 'A'*(blockSize-1)
            textToEncrypt = firstBlock + shortSecondBlock
            encText = AESECBOracle(textToEncrypt, unknownString, j)
            byteDecrypted = P11.AESDetectionOracle(encText)
            if byteDecrypted == True: unknownStringDecrypted += chr(i)
            i += 1
    return unknownStringDecrypted


def main():
    unknownString = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg' \
                    'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq' \
                    'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg' \
                    'YnkK'
    blockSize = discoverBlockSize(unknownString)
    unknownStringDecrypted = decryptUnknownStringByteAtATime(blockSize, unknownString)
    print(unknownStringDecrypted)
    return None


if __name__ == '__main__':
    main()















