#AES in ECB mode decryption only
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

aesKey = b'NO PAIN NO GAIN!'
cipher = Cipher(algorithms.AES(aesKey), modes.ECB(), backend=default_backend())
#message = b'Try this for a change'

'''
This part encrypts my own text for students. The pt is in 7alt.txt
'''
f1 = open('7alt.txt', 'r')
pt = f1.read()
f1.close()

encryptor = cipher.encryptor()
padder = padding.PKCS7(128).padder()
padded_data = padder.update(pt.encode()) + padder.finalize()
textEnc = encryptor.update(padded_data) + encryptor.finalize()
textEnc = base64.b64encode(textEnc)

#write the encrypted text as base64 in the file
f2 = open('7altEnc.txt', 'w')
f2.write(str(textEnc, 'utf-8'))
f2.close()


#read the encrypted text, base64 decode it and then decrypt it
f3 = open('7altEnc.txt', 'r')
ct = f3.read()
f3.close()
ct = base64.b64decode(ct)

decryptor = cipher.decryptor()
textOut = decryptor.update(ct) + decryptor.finalize()  #output is in bytes

print(str(textOut, 'utf-8'))   #convert bytes to string

