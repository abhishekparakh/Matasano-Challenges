#Breaking repeating-key XOR

import base64
import binascii

englishLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', \
                  'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                  'q', 'r', 's', 't', 'u', 'v', 'w', 'x', \
                  'y', 'z']

#returns the hamming weight of the XOR of two strings
#this is called the hamming distance between the strings
#also called the edit distance
def hammingDistance(str1, str2):
    countHammingDist = 0   #initialize counter
    for a,b in zip(str1, str2):    #make tuples and XOR
        countHammingDist += bin(ord(a)^ord(b)).count('1')  #count 1s
    return countHammingDist

def singleCharXORAnalysis(block):
    blockKey = ''
    for l in range(len(englishLetters)):
        out = ''
        for c in block:
            out += chr(ord(c) ^ ord(englishLetters[l]))
        out = out.lower()
        blockKey = englishLetters[l]
        print('key: ', englishLetters[l], ' :: ', out)  # out contains the decrypted string in ascii
    return blockKey

a = 'this is a test'
b = 'wokka wokka!!!'
print(hammingDistance(a,b))

f = open('6decoded.txt', 'r')

#read the file - it contains base64 text so convert to ascii as well
ciphertext = 'KCEtLDorIC5pMyQ3KCgtZSghLSw6KyAuaTMkNygoLWUoIS0sOisgLmkzJDcoKC1lKCEtLDomLmU5IjckIitlJCsrLDYhJi5lOSI3JCIr'
print(ciphertext)
ciphertext = str(base64.b64decode(ciphertext))
ciphertext = ciphertext[2:len(ciphertext)-1]   #remove b' from start and ' from end
print(ciphertext)

#step 3 and 4
distance = dict()    #start a list for distances
#we are storing tuples in the list (distance, keysize)
for KEYSIZE in range(2,15):
    distance1 = hammingDistance(ciphertext[:KEYSIZE], ciphertext[KEYSIZE:KEYSIZE*2])/KEYSIZE
    distance2 = hammingDistance(ciphertext[KEYSIZE*2:KEYSIZE*3], ciphertext[KEYSIZE*3:KEYSIZE*4])/KEYSIZE
    distance[KEYSIZE] = (distance1+distance2)/2
minDistance = min(distance)   #sort the list - it sorts based on first element of the tuple
print(distance)

'''
keySize = minDistance[1]    #second element of the tuple

#step 5
ciphertextBlocks = []
for t in range(0,len(ciphertext),keySize):
    ciphertextBlocks.append(ciphertext[t:t+keySize])

#step 6
block = ''
encryptionKey = ''
for i in range(keySize):
    for t in range(len(ciphertextBlocks)):
        block += ciphertextBlocks[t]
        #step 7 (solve for the first block)
        encryptionKey += singleCharXORAnalysis(block)
'''


