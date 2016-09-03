#AES in ECB mode decryption only
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

aesKey = b'YELLOW SUBMARINE'
#message = b'Try this for a change'

f = open('7.txt', 'r')
ct = f.read()
ct = base64.b64decode(ct)
print(type(ct))

cipher = Cipher(algorithms.AES(aesKey), modes.ECB(), backend=default_backend())

decryptor = cipher.decryptor()
textOut = decryptor.update(ct) + decryptor.finalize()  #output is in bytes

print(str(textOut, 'utf-8'))   #convert bytes to string

