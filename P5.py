#Implement repeating-key XOR
import bitarray

key = "AnotherDayIsHere!!@#"    #Fixed

text = "Another day has almost come and gone, Can't imagine what else" \
       "could go wrong, Sometimes I'd like to hide away somewhere and lock" \
       "the door, A single battle lost but not the war ('cause)!!!"

#f = open('5pt.txt', 'r')
#text = f.read()

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