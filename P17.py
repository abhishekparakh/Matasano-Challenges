#CBC Padding oracle attack
import base64
import P10, P16
from Cryptodome import Util


class webAppCBC:
    def __init__(self):
        self.key = b'YELLOW SUBMARINE'
        self.iv = b'\x00'*16


    def encrypt(self, dataInBytes):
        encTextInBytes = P10.aesCBCMode(dataInBytes, self.key, self.iv, 'e')
        return encTextInBytes


    def decrypt(self, encTextInBytes):
        #padding is checked in P10 right after decryption
        decTextInBytes = P10.aesCBCMode(encTextInBytes, self.key, self.iv, 'd')
        paddingValid = self.checkPadValidity(decTextInBytes)
        if paddingValid == 'PKCS#7 padding is incorrect.':
            return False
        else:
            return True


    def checkPadValidity(self, decryptedText):
        flag = P10.unpadder(decryptedText, 128)
        return flag                #False if the padding is incorrect


class attacker:
    def attackCBCCipher(self, webapp, cipherCBC, blockToDecrypt):

        #print(webapp.decrypt(cipherCBC))

        if len(cipherCBC)/16 <= blockToDecrypt:
            return 'Cipher does not have enough blocks'

        #chop the ciphertext to length blockToDecrypt + 1
        newCipherCBC = cipherCBC[:16*(blockToDecrypt+1)]

        #TODO: hard coded to just do the last byte right now
        #attack byte at a time
        counter = 0
        #xor the current guess into the current byte
        decryptedValue = ''
        for offset in range(15, -1, -1):
            frontPart = ('\x00'*offset).encode()
            endPart = decryptedValue.encode()
            for i in range(255):
                validPaddingThisRound = frontPart + bytes([16-offset])*(16-offset)
                currentGuess = frontPart + bytes([i]) + endPart
                valueToXor1 = ('\x00'*(16*(blockToDecrypt-1))).encode() + currentGuess + ('\x00'*16).encode()
                valueToXor2 = ('\x00'*(16*(blockToDecrypt-1))).encode() + validPaddingThisRound + ('\x00'*16).encode()
                valueToXor = P16.xorBytes(valueToXor1, valueToXor2)
                modifiedCipher = P16.xorBytes(valueToXor, newCipherCBC)
                decSuccess = webapp.decrypt(modifiedCipher)
                if decSuccess == True:
                    #found the byte value, save it
                    decryptedValue = str(bytes([i]), 'latin1') + decryptedValue
                    #continue to try next byte
                    break
                #if decSuccess == False:
                #    print("Decryption failed!")
        print(decryptedValue)
        return 'here'


def main():
    #inputText = b'YELLOW SUBMARINEYELLOW SUBMARINEyellow submarine'
    inputText = b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl"
    unknownText = base64.b64decode(inputText)


    webapp = webAppCBC()
    encData = webapp.encrypt(unknownText)

    attack = attacker()
    attack.attackCBCCipher(webapp, encData, 2)    #attacking first block decrypts second block, so on



    #decData = webapp.decrypt(encData)

    #print(decData)






if __name__ == '__main__':
    main()


