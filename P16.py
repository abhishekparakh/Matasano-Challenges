#CBC bit-flipping attacks
import P10, P9            #P9 had padding, P10 has CBC
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


prependText = "comment1=cooking%20MCs;userdata="
appendText = ";comment2=%20like%20a%20pound%20of%20bacon"
AESKeyLength = 16  # size in bytes
key = b'YELLOW SUBMARINE' #os.urandom(AESKeyLength)  # generate random key and fix it for this program
iv = os.urandom(AESKeyLength)


#Quote out ; and = from the input text before encrypting with CBC
def sanitizeInput(inputText):
    inputText = inputText.replace(';', '')
    inputText = inputText.replace('=', '')
    return inputText


#function 1
def function1Enc(inputText):     #inputText comes from user
    dataToEncryptBeforeSanitization = prependText + inputText + appendText
    dataToEncrypt = sanitizeInput(dataToEncryptBeforeSanitization)
    encryptedData = P10.aesCBCMode(dataToEncrypt.encode(), key, iv, 'e')  #returns bytes
    return encryptedData    #returns bytes


#function 2
def function2Enc(encryptedTextInBytes):
    decryptedData = P10.aesCBCMode(encryptedTextInBytes, key, iv, 'd')  #returns string
    print(decryptedData)
    try:
        splitData = decryptedData.split(';')
    except ValueError:
        print('String could not be split at ;')
        return False
    for t in splitData:
        try:
            attribute, value = t.split('=')
        except ValueError:
            continue
        if attribute == 'admin':
            return True
    return False


#XOR bytes and return bytes
def xorBytes(aInBytes, bInBytes):     #encode() was increasing the output length for some reason!
    out = b''
    for s,t in zip(aInBytes,bInBytes):
        out += bytes([s^t])     #this converts ints to bytes
    return out


#attack the ciphertext. XOR appropriate bytes into the ciphertext such that next block changes
def attackTheCipherText(encryptedData):
    valueToXOR = 'c9<516e,*-=c'.encode()     #this xored with Xs gives ;admin=true;
    # TODO: XOR the value into the block not replace the block, duh!
    modifiedEncryptedData = encryptedData     #just initializing
    offset = 0
    while function2Enc(modifiedEncryptedData)!=True:
        start = encryptedData[0:offset]
        middle = encryptedData[offset:offset+len(valueToXOR)]
        end = encryptedData[offset+len(valueToXOR):]
        modifiedEncryptedData = start + xorBytes(valueToXOR, middle) + end
        offset += 1
        print(offset)
    return function2Enc(modifiedEncryptedData)


#TODO: Bonus exercise - write a code to figure out block size in CBC mode. In ECB it is very easy, not do for CBC
#TODO: Here it works with offset of 13 because after sanitization prepend text is 29 in length.
#TODO: The moment it reaches 13, out attack block xors into the next full block in prepend text and causes user data
#TODO: to turn into ;admin=true;

#TODO: Bonus exercise - make this work for 3DES instead of AES


def main():
    userData = 'X'*16*3        #fill in three blocks of Xs
    encryptedData = function1Enc(userData)
    print(attackTheCipherText(encryptedData))





if __name__ == '__main__':
    main()