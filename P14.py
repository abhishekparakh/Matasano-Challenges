#Byte-at-a-time ECB decyrption (harder)
import P10, P11
import os
import base64
import random

'''unknownString = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg' \
                'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq' \
                'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg' \
                'YnkK'''
#unknownString = 'V2hlbiBJIHdhcyBhIGxpdHRsZSBiaXR0eSBiYWJ5DQpNeSBtYW1hIHdvdWxkIHJvY2sgbWUgaW4gdGhlIGNyYWRsZSwNCkluIHRoZW0gb2xkIGNvdHRvbiBmaWVsZHMgYmFjayBob21lOw0KSXQgd2FzIGRvd24gaW4gTG91aXNpYW5hLA0KSnVzdCBhYm91dCBhIG1pbGUgZnJvbSBUZXhhcmthbmEsDQpJbiB0aGVtIG9sZCBjb3R0b24gZmllbGRzIGJhY2sgaG9tZS4='
f = open('C:\\Users\\aparakh\\Box Sync\\Class Fall 2016\\Applied Cryptography\\Week 4\\p11.txt', 'r')
unknownString = f.read()

AESKeyLength = 16  # size in bytes
key = os.urandom(AESKeyLength)  # generate random key and fix it for this program
randomNoOfBytesToPrepend = random.randrange(5,10)

#ECB encryption oracle that adds random data before the input data
#and adds the target string after the input data
def AESECBOraclePrependAndAppend(data, offset):
    dataToPrepend = os.urandom(randomNoOfBytesToPrepend)    #add random 10-20 bytes before the data
    dataInBytes = dataToPrepend + data.encode() + base64.b64decode(unknownString)[offset:]  #append the random string before encrypting
    encOut = P10.aesECBMode(dataInBytes, key,'e')   #reusing functions from P10
    return encOut          #returns bytes if generateKeyStream (flag = e)


#discover block size by looking at output size jump:
#it jumps right on the boundary because dummy block is added in PKCS#7
def discoverBlockSize():
    flag = 0            #flag is set once block size is discovered
    repeat = 1       #start with a block size of 1 byte, increments in 1 byte as well
    pastEncTextSize = -1      #track the output size of the encryption function
    while flag == False:
        text = 'A' * repeat
        encText = AESECBOraclePrependAndAppend(text, offset=0)       #encText is in bytes
        if pastEncTextSize < 0:
            pastEncTextSize = len(encText)     #save the current size as past value
        elif len(encText) > pastEncTextSize:
            flag = True
            blockSize = len(encText) - pastEncTextSize
        if flag == False: repeat += 1            #if ECB not found, increment block size
        pastEncTextSize = len(encText)
    return blockSize   #returns block size as integer


#since the encryption function prepends random bytes
#we want to find out how many bytes that is
#this will give us the boundary of the first part of the byte
def howShortIsFirstRandomPart(blockSize):
    numberOfPaddingBytesFirstPart = 0
    #create two blocks that will cause ECB detection for sure
    block1 = 'A' * blockSize
    block2 = 'A' * blockSize
    #not stuff bytes in the front one at a time and detect ECB
    ECBDetected = False
    while(ECBDetected == False):
        inputBlocks = 'X' * numberOfPaddingBytesFirstPart + block1 + block2
        encText = AESECBOraclePrependAndAppend(inputBlocks, offset=0)
        ECBDetected = P11.AES_ECBDetectionOracle(encText)
        if ECBDetected:
            return numberOfPaddingBytesFirstPart
        else:
            numberOfPaddingBytesFirstPart += 1
    return numberOfPaddingBytesFirstPart


#this function takes in the blockSize that was computed and
#decrypts the unknown string
def decryptUnknownStringByteAtATime(blockSize):
    numberOfPaddingBytesFirstPart = howShortIsFirstRandomPart(blockSize)
    if numberOfPaddingBytesFirstPart < 16:
        paddingToEvenThingsOut = 'X' * numberOfPaddingBytesFirstPart
    #craft a byte short input
    unknownStringDecrypted = ''
    for j in range(0, len(unknownString)):  #j chops off unknownString as it is decrypted
        i = 0
        ECBDetected = False
        while ECBDetected == False:
            firstBlock = 'A'*(blockSize-1) + chr(i)
            shortSecondBlock = 'A'*(blockSize-1)
            textToEncrypt = paddingToEvenThingsOut + firstBlock + shortSecondBlock
            encText = AESECBOraclePrependAndAppend(textToEncrypt, j)    #j is the offset that increments as a byte is decrypted
            ECBDetected = P11.AES_ECBDetectionOracle(encText)
            if ECBDetected == True:
                unknownStringDecrypted += chr(i)
            i += 1
    return unknownStringDecrypted     #return decrypted string


def main():
    blockSize = discoverBlockSize()
    unknownStringDecrypted = decryptUnknownStringByteAtATime(blockSize)
    print(unknownStringDecrypted)
    return None


if __name__ == '__main__':
    main()
