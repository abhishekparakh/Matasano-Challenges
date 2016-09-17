#Implement CTR, the stream cipher mode
import sys
from struct import *
import base64
from Cryptodome.Cipher import AES
from bitstring import BitArray


class CounterMode:
    def __init__(self, key, nonce):
        self.nonce = nonce
        self.key = key
        self.counterValue = 0       #just the initial counter value
        self.counter = pack('<Q', self.counterValue)  # < makes sure it is little endian, Q makes it 8 bytes unsigned long long
        self.inputToEnc = nonce + self.counter     #in bytes


    #generateKeyStream maintains state of the counter
    def generateKeyStream(self):
        encryptor = AES.new(self.key, AES.MODE_ECB)
        outEnc = encryptor.encrypt(self.inputToEnc)
        #increment counter and then the
        self.counterValue += 1
        self.counter = pack('<Q', self.counterValue)
        self.inputToEnc = self.nonce + self.counter   #used next time it is invoked
        return outEnc


    #decrypt byte at a time
    def decrypt(self, dataInBytes):       #input as bytes
        #this is using builtin function, counter increments are not the same!
        #decryptor = AES.new(self.key, AES.MODE_CTR, nonce = self.nonce)
        #decOut = decryptor.encrypt(dataInBytes)    #this is returned

        decrypted = ''
        for i in range(0, len(dataInBytes), 16):
            currentChunk = dataInBytes[i:i+16]  #get 16 byte chunks
            currentChunkHex = currentChunk.hex()
            currentChunkBin = BitArray(hex=currentChunkHex).bin

            valueToXOR = self.generateKeyStream()    #get encrypted counter value
            valueToXORHex = valueToXOR.hex()
            valueToXORBin = BitArray(hex=valueToXORHex).bin

            for a,b in zip(valueToXOR, currentChunk):
                decrypted += chr(a^b)      #xor bytes and convert to chr
        return decrypted       #returns a string always


    #encrypt the input string
    def encrypt(self, dataInBytes):
        #this is using builtin function, counter increments are not the same!
        #encryptor = AES.new(self.key, AES.MODE_CTR, nonce = self.nonce)
        #outEnc = encryptor.encrypt(dataInBytes)    #this is returned

        #below is my function
        encOut = '0b'
        for i in range(0, len(dataInBytes), 16):
            currentChunk = dataInBytes[i:i+16]
            currentChunkHex = currentChunk.hex()
            currentChunkBin = BitArray(hex=currentChunkHex).bin

            valueToXOR = self.generateKeyStream()
            valueToXORHex = valueToXOR.hex()
            valueToXORBin = BitArray(hex=valueToXORHex).bin

            for a,b in zip(valueToXORBin, currentChunkBin):
                encOut += str(int(a)^int(b))   #.to_bytes(1, byteorder=sys.byteorder)

            encOutBytes = BitArray(encOut).bytes
        return(encOutBytes)              #encOut is in bytes


def main():
    # initialize
    key = b'YELLOW SUBMARINE'
    nonce = pack('<Q', 0) # < makes sure it is little endian, Q makes it 8 bytes unsigned long long

    data = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    dataInBytes = base64.b64decode(data)
    print(data)

    CTRMode = CounterMode(key, nonce)        #initilize the counter mode
    decOut = CTRMode.decrypt(dataInBytes)

    CTRMode = CounterMode(key, nonce)        #reinitilize the counter mode
    encOut = CTRMode.encrypt(decOut.encode())
    print(str(base64.b64encode(encOut),'utf-8'))






if __name__ == '__main__':
    main()