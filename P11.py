#An ECB/CBC detection oracle

import P10   #my implementation of AES CBC mode
import os
import random


#Note: sometimes detection fails even though it is ECB
#because there may be no repetitive blocks in the plaintext
def AES_ECBDetectionOracle(dataInBytes):    #data is in bytes
    flag = False
    chunks = [dataInBytes[i:i + 16] for i in range(0, len(dataInBytes), 16)]
    for i in range(len(chunks)):
        count = chunks.count(chunks[i])   #count repetition of chunks
        if count>=2:
            flag = True      #ECB mode found
            break
    return flag


def AESECBOracle(dataInBytes):
    AESKeyLength = 16   #size in bytes
    key = os.urandom(AESKeyLength)   #generate random key
    encOut = P10.aesECBMode(dataInBytes, key,'e')   #reusing functions from P10
    return encOut          #returns bytes if encrypt (flag = e)


def AESCBCOracle(dataInBytes):
    AESKeyLength = 16     #size in bytes
    AESBlockLength = 16   #size in bytes
    key = os.urandom(AESKeyLength)  # generate random key
    iv = os.urandom(AESBlockLength)   #generate random iv
    encOut = P10.aesCBCMode(dataInBytes, key, iv, 'e')
    return encOut       #returns bytes if encrypt (flag = e)


#append 5-10 bytes before and after the plaintext
def randomAddData(dataInBytes, prependFlag, appendFlag):  #incoming data in bytes
    bytesToPrepend = os.urandom(random.randrange(5,10))   #generate random bytes to prepend
    bytesToAppend = os.urandom(random.randrange(5,10))    #generate random bytes to append
    if prependFlag:
        dataInBytes = bytesToPrepend + dataInBytes    #it is okay to concatenate bytes to bytes together
    if appendFlag:
        dataInBytes = dataInBytes + bytesToAppend     #it is okay to concatenate bytes to bytes together
    return dataInBytes


def encryptionOracle(dataInBytes):
    coinToss = random.randint(0,1)
    if coinToss:
        encDataECB = AESECBOracle(dataInBytes)
        print("ECB mode chosen")
        return encDataECB      #encrypted data is in bytes
    else:
        encDataCBC = AESCBCOracle(dataInBytes)
        print("CBC mode chosen")
        return encDataCBC      #encrypted data is in bytes


def main():
    f = open('11.txt', 'r')   #read file
    data = f.read()
    dataInBytes = data.encode()   #convert data input bytes

    #add random data before and after
    inputWithRandomDataAdded = randomAddData(dataInBytes, prependFlag=1, appendFlag=1)

    #Encrypt data 1/2 the time with ECB and other 1/2 the time with CBC
    out = encryptionOracle(inputWithRandomDataAdded)

    ECBFound = AES_ECBDetectionOracle(out)
    print("ECBDetected: ", ECBFound)


if __name__ == "__main__":
    main()













