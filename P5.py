#Implement repeating-key XOR
import bitarray

key = 'ICE'    #Fixed

text = "We didn't start the fire, " \
    "It was always burning, " \
    "Since the world's been turning, " \
    "We didn't start the fire, " \
    "No we didn't light it, " \
    "But we tried to fight it, "

l = len(text)

#Repeate the key so that it is as long as the length of the text
keyExpanded = key*(l//len(key)) + key[:l%len(key)]

#To XOR the text and the key, make tuples of characters one from each
#then convert the characters to numbers (ord()) and ^ them
#then convert to hex using (hex()) and replace the 0x prefix
encryptedOut = ''
for a,b in zip(text,keyExpanded):
    encryptedOut += chr(ord(a)^ord(b))

print((encryptedOut.encode()).hex())