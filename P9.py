#Challenge 9
#Implement PKCS#7 padding

from cryptography.hazmat.primitives import padding


def padderPKCS7(inputText, blockSizeInBits):    #inputText is ASCII
    padder = padding.PKCS7(blockSizeInBits).padder()
    padded_data = padder.update(inputText.encode()) + padder.finalize()
    return padded_data      #returns bytes


def unpadderPKCS7(inputTextInBytes, blockSizeInBits):     #inputText in bytes
    unpadder = padding.PKCS7(blockSizeInBits).unpadder()
    unpadded_data = unpadder.update(inputTextInBytes) + unpadder.finalize()


def main():
    blockSizeInBits = 160
    text = 'This is a Saturday'
    print(padderPKCS7(text, blockSizeInBits))


if __name__ == "__main__":
    main()