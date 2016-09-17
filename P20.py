#Break fixed-nonce CTR statistically
import P18, P6
import os, sys
import base64
from struct import *
from Cryptodome.Cipher import AES
from bitstring import BitArray


keylength = 16
random = b'asdfasdf' #os.urandom(keylength)
print('Real random key: ', str(random, 'latin1'))
randomHex = random.hex()
Brandom = BitArray(hex=randomHex).bin
#print('Real key in bits: ', Brandom)

def encrypt(dataInBytes, key, nonce):
    #CTRMode = P18.CounterMode(key, nonce)
    #encOutBytes = CTRMode.encrypt(dataInBytes)

    #this is using builtin function
    #encryptor = AES.new(key, AES.MODE_CTR, nonce = nonce)
    #encOut = encryptor.encrypt(dataInBytes)    #this is returned

    #temporary XOR function for debugging
    #random = ('%^&'*len(dataInBytes)).encode()
    random = ''
    #for t in range(1):
    #    random += str(base64.b64encode(randomBytes), 'utf-8')

    random = (Brandom * len(dataInBytes))
    encOut = '0b'
    data = BitArray(dataInBytes).bin
    for a, b in zip(data, random):
        encOut += str(int(a)^int(b))
    encOutBytes = BitArray(encOut).bytes
    return encOutBytes                    #return value in bytes


def main():
    # initialize
    key = b'YELLOW SUBMARINE'
    nonce = pack('<Q', 0)  # < makes sure it is little endian, Q makes it 8 bytes unsigned long long

    encLines = list()
    lowestLen = 50000
    f = open('20alt.txt', 'r')
    for line in f:
        #data = base64.b64decode(line)
        #print(str(data))
        #truncate lines to multiples of 16
        lineLen = len(line)//keylength*len(line)
        line = line[:lineLen]

        encOut = encrypt(line.encode(), key, nonce)
        encLines.append(encOut)
        if len(encOut)< lowestLen:
            lowestLen = len(encOut)
        lowestLen = lowestLen//keylength*keylength

    #truncate ciphertexts to lowest length ciphertexts
    oneLongCiphertext = b''        #all in bytes
    for i in range(len(encLines)):
        encLines[i] = encLines[i][:lowestLen]     #encLines are in bytes
        #print(len(encLines[i]), ' :', encLines[i])
        #concatenate the truncated ciphertexts
        oneLongCiphertext += encLines[i]
        #print(oneLongCiphertext)

    #decrypt using P6 implementation
    decryptOut = P6.decrypt(oneLongCiphertext)

    print(decryptOut)


if __name__ == "__main__":
    main()