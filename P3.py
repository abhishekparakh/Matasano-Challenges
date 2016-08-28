#Single-byte XOR cipher
import binascii

englishFrequency = {
    'e':0.1202, 't':0.09, 'a':0.0812, 'o':0.0768, 'i':0.0731, 'n':0.0695,
    's':0.0628, 'r':0.0602, 'h':0.0592, 'd':0.0432, 'l':0.0398, 'u':0.0288,
    'c':0.0271, 'm':0.0261, 'f':0.0230, 'y':0.0211, 'w':0.0209, 'g':0.0203,
    'p':0.0182, 'b':0.0149, 'v':0.0111, 'k':0.0069, 'x':0.0017, 'q':0.0011,
    'j':0.0010, 'z':0.0007
}

#using only the two few characters to check for requencies
vowels = ['e', 't', 'a', 'o', 'i', 'u']

englishLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', \
                  'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                  'q', 'r', 's', 't', 'u', 'v', 'w', 'x', \
                  'y', 'z']

hex = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
h = binascii.unhexlify(hex).decode('ascii')   #h is of type string


key = ''
for l in range(len(englishLetters)):
    out = ''
    for c in h:
        out += chr(ord(c) ^ ord(englishLetters[l]))
    out = out.lower()
    print('key: ', englishLetters[l], ' :: ', out)   #out contains the decrypted string in ascii


'''
    #check character frequencies
    #as soon as the match is found - stop
    for t in range(len(vowels)):
        count = out.count(vowels[t])
        frequency = count/len(out)
        print("count: ", count, "char: ", vowels[t], "frequency: ", frequency)
        print(englishFrequency[vowels[t]] - frequency)
        if abs(englishFrequency[vowels[t]] - frequency) <= 0.001:
            print('output: ', out)
            print('key: ', key)
            break
'''


#print(binascii.b2a_uu(binascii.unhexlify(hex)))

