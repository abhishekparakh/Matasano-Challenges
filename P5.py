#Implement repeating-key XOR
import bitarray

key = 'ICEE'    #Fixed

text = 'abhishek parakh abhishek parakh abhishek parakh abhisek parakh abhishek parakh'

l = len(text)

#Repeate the key so that it is as long as the length of the text
keyExpanded = key*(l//len(key)) + key[:l%len(key)]

#To XOR the text and the key, make tuples of characters one from each
#then convert the characters to numbers (ord()) and ^ them
#then convert to hex using (hex()) and replace the 0x prefix
encryptedOut = ''
for a,b in zip(text,keyExpanded):
    encryptedOut += hex(ord(a)^ord(b)).replace('0x','')

print(encryptedOut)