#Implementing ECB and CBC modes for AES

from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

class AESECB:
    def __init__(self, key):
        self.key = key
        self.blockLenInBytes = 16

    def padder(self, textInBytes):
        pad = Padding.pad()


    def encrypt(self, textInBytes):
        encryptor = AES.new(self.key, AES.MODE_ECB)
        encOutInBytes = encryptor.encrypt(textInBytes)
        return encOutInBytes

    def decrypt(self, cipherInBytes):
        decryptor = AES.new(self.key, AES.MODE_ECB)
        decOutInBytes = decryptor.decrypt(cipherInBytes)
        return decOutInBytes


def main():
    key = b'YELLOW SUBMARINE'
    text = b'yellow submarine'
    aes = AESECB(key)
    encOut = aes.encrypt(text)
    print(encOut)
    decOut = aes.decrypt(encOut)
    print(decOut)








if __name__ == '__main__':
    main()
