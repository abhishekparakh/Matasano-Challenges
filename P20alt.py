import base64
from Cryptodome.Cipher import AES
import P6

key = b'YELLOW SUBMARINE'
nonce = b'\x00'*15

f = open('20.txt', 'r')

encLine = list()
for line in f:
    encryptor = AES.new(key, AES.MODE_CTR, nonce=nonce)
    dataInBytes = base64.b64decode(line)
    encLine.append(encryptor.encrypt(dataInBytes))    #this is returned


#truncate to shortest ciphertext length
lowestLen = 50000
for item in encLine:
    #print(item)
    if len(item)<lowestLen:
        lowestLen = len(item)

encList = list()
oneLongCipher = b''
for item in encLine:
    encList.append(item[:lowestLen])
    oneLongCipher += item[:lowestLen]

decryptOut = P6.decrypt(oneLongCipher)

print(decryptOut)