#Recover the key from CBC with IV=key
import os, P10
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


AESKeyLength = 16  # size in bytes
BlockLength = 16
key = b'YELLOW SUBMARINE' #os.urandom(AESKeyLength)  # generate random key and fix it for this program
iv = key   #os.urandom(AESKeyLength)

dataToEncrypt = b'abcdefghijklmnop1234567891234567ponmlkjihghedcba'   #at least 3 blocks long

'''
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
ct = encryptor.update(dataToEncrypt) + encryptor.finalize()
'''

encryptedData = P10.aesCBCMode(dataToEncrypt, key, iv, 'e')  # returns bytes, function will add a padding block

#attack the cipher
#C1, C2, C3, PB -> C1, 0, C1, PB
#divided the cipher into blocks
chunks = [encryptedData[i:i + BlockLength] for i in range(0, len(encryptedData), BlockLength)]
#set the third chunk = first chunk and the second chunk to zero
n=0
chunks[n+2] = chunks[n]
chunks[n+1] = b'\x00'*16
#join all the chunks together again
modifiedEncryptedData = b''.join(chunks)

#decrypt the modified data
decryptedData = P10.aesCBCMode(modifiedEncryptedData, key, iv, 'd')

#chunk up the decrypted data and do P1 xor P3 to get the key
chunksDecryptedData = [decryptedData[i:i + BlockLength] for i in range(0, len(decryptedData), BlockLength)]

retrievedKey = ''
for a, b in zip(chunksDecryptedData[n], chunksDecryptedData[n+2]):
    retrievedKey += chr(ord(a)^ord(b))

print(retrievedKey)















