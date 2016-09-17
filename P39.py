#Implement RSA

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


pt = "secret"
key = RSA.generate(2048)

encryptor = PKCS1_OAEP.new(key)
out = encryptor.generateKeyStream(pt.encode())

decryptor = PKCS1_OAEP.new(key)
dout = decryptor.decrypt(out)






