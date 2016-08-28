#Breaking repeating-key XOR

import base64
import math

#returns the hamming weight of the XOR of two strings
#this is called the hamming distance between the strings
#also called the edit distance
def hammingDistance(str1, str2):   #input must be bytes
    countHammingDist = 0   #initialize counter
    for a,b in zip(str1, str2):    #make tuples and XOR
        countHammingDist += bin(a^b).count('1')  #count 1s
    return countHammingDist

a = 'is this heaven '
b = "no it’s iowa!!"
print(hammingDistance(a.encode(),b.encode()))

def findKey(text):
    # Trying to break the cipher by counting characters
    # Looking for most commonly occurring character (e) and then finding out what it is xored with to get the key
    charFreq = dict()
    for c in text:
        if c not in charFreq:
            charFreq[c] = 1
        else:
            charFreq[c] += 1
    # Find the most commonly occurring character
    currentHighest = -1
    charHighest = ''
    for t in charFreq:
        if charFreq[t] > currentHighest:
            currentHighest = charFreq[t]
            charHighest = t
    print(charHighest)
    key = chr(charHighest ^ ord(' '))  # space is the most common character
    return key

def main():
    f = open('6.txt', 'r')

    #read the file - it contains base64 text so convert to ascii as well
    ciphertext = f.read()
    #ciphertext = 'dGhpcyBpcyBhIHRlc3R3b2trYSB3b2trYSEhIQ=='
    ciphertext = base64.b64decode(ciphertext)

    #step 3 and 4
    distance = dict()    #start a list for distances
    #we are storing tuples in the list (distance, keysize)
    for KEYSIZE in range(2,40):
        distTemp = 0
        count = 0
        chunks = [ciphertext[i:i+KEYSIZE] for i in range(0, len(ciphertext), KEYSIZE)]
        print(len(chunks))
        for i in range(len(chunks)-1):
            distTemp += hammingDistance(chunks[i], chunks[i+1])/KEYSIZE
        distance[KEYSIZE] = distTemp/len(chunks)
    keySize = sorted(distance, key=distance.get)[0]   #get the first element from the sorted list

    #Make groups of every keySize th item from the ciphertext
    #And do single character xor analysis on it
    key = ''
    for i in range(keySize):
        chunk = ciphertext[i::keySize]
        key += findKey(chunk)

    print("They key is: ", key)

    #Decrypt the ciphertext
    keyBytes = key.encode()
    #repeat the keyBytes. It ends up longer but that's okay zip will truncate it
    keyBytesRepeat = keyBytes*math.ceil(len(ciphertext)/len(keyBytes))
    decryptOut = ''
    for a, b in zip(keyBytesRepeat, ciphertext):
        decryptOut += chr(a^b)

    print("Decrypted plaintext: ")
    print(decryptOut)


if __name__ == '__main__':
    main()

