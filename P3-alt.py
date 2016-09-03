#Single-byte XOR cipher

import binascii
import sys
from bitstring import BitArray

#using only the two few characters to check for frequencies
vowels = ['e', 't', 'a', 'o', 'i', 'u']

englishLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', \
                  'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                  'q', 'r', 's', 't', 'u', 'v', 'w', 'x', \
                  'y', 'z']

#Decryption part
string = '26294f2e4f222e214f263c4f2029292a3d2a2b4f2e4f292e2c3b4f3827262c274f28202a3c4f2e282e26213c3b4f27263c4f26213c3b26212c3b3c4f272a4f382623234f3c2c3d3a3b262126352a4f263b4f2c23203c2a23364f2e212b4f3a21232a3c3c4f3b272a4f2a39262b2a212c2a4f263c4f20392a3d38272a23222621284f272a4f382623234f3d2a293a3c2a4f3b204f2d2a23262a392a4f263b4f26294f20214f3b272a4f203b272a3d4f272e212b4f272a4f263c4f2029292a3d2a2b4f3c20222a3b272621284f3827262c274f2e2929203d2b3c4f2e4f3d2a2e3c20214f29203d4f2e2c3b2621284f26214f2e2c2c203d2b2e212c2a4f3b204f27263c4f26213c3b26212c3b3c4f272a4f382623234f2e2c2c2a3f3b4f263b4f2a392a214f20214f3b272a4f3c232628273b2a3c3b4f2a39262b2a212c2a4f3b272a4f203d262826214f20294f22363b273c4f263c4f2a373f232e26212a2b4f26214f3b27263c4f382e36'
text = bytes.fromhex(string).decode('utf-8')
print(text)

#Trying to break the cipher by counting characters
#Looking for most commonly occurring character (e) and then finding out what it is xored with to get the key
charFreq = dict()
for c in text:
    if c not in charFreq:
        charFreq[c] = 1
    else:
        charFreq[c] += 1
#Find the most commonly occurring character
currentHighest = -1
charHighest = ''
for t in charFreq:
    if charFreq[t] > currentHighest:
        currentHighest = charFreq[t]
        charHighest = t
#print(charHighest)
#print(currentHighest)
print('key: ', chr(ord(charHighest) ^ ord(' ')))   #space is the most common character

#Decryption part ends

#Encryption part starts
#text = 'IF A MAN IS OFFERED A FACT WHICH GOES AGAINST HIS INSTINCTS HE WILL ' \
 #      'SCRUTINIZE IT CLOSELY AND UNLESS THE EVIDENCE IS OVERWHELMING HE WILL ' \
  #     'REFUSE TO BELIEVE IT IF ON THE OTHER HAND HE IS OFFERED SOMETHING WHICH ' \
   #    'AFFORDS A REASON FOR ACTING IN ACCORDANCE TO HIS INSTINCTS HE WILL ACCEPT ' \
    #   'IT EVEN ON THE SLIGHTEST EVIDENCE THE ORIGIN OF MYTHS IS EXPLAINED IN THIS WAY'
#print(text)
#Encryption part ends

for k in englishLetters:
    out = ''
    for c in text:
        out += chr(ord(k)^ord(c))
    print("key: ", k, ' Decryption: ', out)        #prints ASCII characters   (used during decryption)
    #out = out.encode()    #convert to bytes like object   #for encryption
    #print(out.hex())       #convert bytes like objects to hex   #for encryption






