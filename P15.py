#PKCS#7 padding validation
import sys

def checkPaddingValidity(text):
    length = len(text)
    lastByte = text[-1]
    #print(ord(lastByte))
    try:             #throw an exception if pad is invalid
        for t in range(-1, -ord(lastByte)-1, -1):
            if lastByte != text[t]:
                raise ValueError
    except ValueError:     #catch the exception - used an inbuilt type
        return 'Invalid Pad!'       #make sure you return else it will execute outer statements
    return 'Valid Pad!'

def main():
    text = "ICE ICE BABY\x04\x04\x04\x04"   #input string
    print(checkPaddingValidity(text))


if __name__ == '__main__':
    main()
