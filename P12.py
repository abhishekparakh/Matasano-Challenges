#Byte-at-a-time ECB decryption
import P10, P11   #my implementation of AES CBC mode
import os
import base64


AESKeyLength = 16  # size in bytes
key = os.urandom(AESKeyLength)  # generate random key and fix it for this program
def AESECBOracleAppendBytes(data, unknownString, offset):
    dataInBytes = data.encode() + base64.b64decode(unknownString)[offset:]  #append the random string before encrypting
    encOut = P10.aesECBMode(dataInBytes, key,'e')   #reusing functions from P10
    return encOut          #returns bytes if encrypt (flag = e)


#discover block size by looking at output size jump: it jumps right on the boundary because dummy block added
def discoverBlockSize(unknownString):
    flag = 0            #flag is set once block size is discovered
    repeat = 1       #start with a block size of 1 byte, increments in 1 byte as well
    pastEncTextSize = -1      #track the output size of the encryption function
    while flag == False:
        text = 'A' * repeat
        encText = AESECBOracleAppendBytes(text, unknownString, offset=0)       #encText is in bytes
        if pastEncTextSize < 0:
            pastEncTextSize = len(encText)     #save the current size as past value
        elif len(encText) > pastEncTextSize:
            flag = True
            blockSize = len(encText) - pastEncTextSize   #difference between two the size before and after
        if flag == False: repeat += 1            #if ECB not found, increment block size
        pastEncTextSize = len(encText)
    return blockSize                     #returns an integer


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
            encText = AESECBOracleAppendBytes(textToEncrypt, unknownString, j)
            byteDecrypted = P11.AES_ECBDetectionOracle(encText)
            if byteDecrypted == True: unknownStringDecrypted += chr(i)
            i += 1
    return unknownStringDecrypted


def main():
    '''unknownString = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg' \
                    'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq' \
                    'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg' \
                    'YnkK'''
    #unknownString = 'V2hlbiBJIHdhcyBhIGxpdHRsZSBiaXR0eSBiYWJ5DQpNeSBtYW1hIHdvdWxkIHJvY2sgbWUgaW4gdGhlIGNyYWRsZSwNCkluIHRoZW0gb2xkIGNvdHRvbiBmaWVsZHMgYmFjayBob21lOw0KSXQgd2FzIGRvd24gaW4gTG91aXNpYW5hLA0KSnVzdCBhYm91dCBhIG1pbGUgZnJvbSBUZXhhcmthbmEsDQpJbiB0aGVtIG9sZCBjb3R0b24gZmllbGRzIGJhY2sgaG9tZS4='
    f = open('C:\\Users\\aparakh\\Box Sync\\Class Fall 2016\\Applied Cryptography\\Week 4\\p11.txt', 'r')
    unknownString = f.read()
    blockSize = discoverBlockSize(unknownString)
    unknownStringDecrypted = decryptUnknownStringByteAtATime(blockSize, unknownString)
    print(unknownStringDecrypted)
    return None


if __name__ == '__main__':
    main()















