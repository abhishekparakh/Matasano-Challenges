#Detect AES in ECB mode
import base64
import binascii

f = open('8.txt', 'r')

lineNumber = 1
for ct in f:     #this reads a line at a time and puts it in ct
    #this is a line in hex, therefore two characters form a byte
    #print(ct)

    #AES ECB uses 16 bytes chunks so to detect ECB check for repetition of 16 byte chunks
    blockSize = 16*2    #16 bytes for regular AES block, since hex, multiply 2
    for t in range(0, len(ct), blockSize):
        currentBlock = ct[t:t+blockSize]
        #print(currentBlock)
        count = ct.count(currentBlock)
        print(count)
        if count>=2:
            print('ECB mode detected in line: ', lineNumber)
            break
    lineNumber += 1
    print(lineNumber)

f.close()

