#Challenge 9
#Implement PKCS#7 padding

from cryptography.hazmat.primitives import padding

blockSizeInBits = 160

text = 'This is a Saturday'

padder = padding.PKCS7(blockSizeInBits).padder()
padded_data = padder.update(text.encode()) + padder.finalize()

print(padded_data)