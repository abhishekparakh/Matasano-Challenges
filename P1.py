# Convert hex to base64

# Create a dictionary for hex to binary
h2b = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', \
       '5':'0101', '6':'0110', '7':'0111', '8':'1000', '9':'1001', \
       'a':'1010', 'b':'1011', 'c':'1100', 'd':'1101', 'e':'1110', \
       'f':'1111'}

# Create a list for base64 characters
b64list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', \
           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', \
           'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', \
           'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', \
           '9', '+', '/', '=']


def b2dec(string):
    # We will get 6-bit strings that need to be converted
    num = 0
    k=0
    for i in range(len(string)-1,-1,-1):
        num = num+int(string[i])*(2**k)
        k += 1
    return num


def b64Convert(hexNum):
    # Pad with 0s if the length is not a multiple of 6 hex characters
    numOfPaddingNibbles = 0  # need this to figure out how many = to put in
    if len(hexNum) % 6 != 0:
        numOfPaddingNibbles = 6 - len(hexNum) % 6
        hexNum = hexNum + '0' * numOfPaddingNibbles

    b64Out = ''
    # Take 6 hex characters at a time
    for i in range(0, len(hexNum), 6):
        slice = hexNum[i:i + 6]
        hex2bin = ''  # convert slice to 24-bit binary string
        for h in slice:
            hex2bin += h2b[h]
        for b in range(0, len(hex2bin), 6):  # take 6-bits at a time to dec
            decNum = b2dec(hex2bin[b:b + 6])
            b64Out += b64list[decNum]

    # ignore cases of numOfPaddingNibbles = 0, 1, and 3
    if numOfPaddingNibbles == 2:
        b64Out = b64Out[:-1] + '='
    if numOfPaddingNibbles == 4:
        b64Out = b64Out[:-2] + '=='

    return b64Out


def main():
    hexNum = '28212d2c3a2b202e6933243728282d6528212d2c3a2b202e6933243728282d6528212d2c3a2b202e' \
             '6933243728282d6528212d2c3a262e6539223724222b65242b2b2c3621262e6539223724222b'
   #input('>>Provide a hex input: ')
    b64Out = b64Convert(hexNum)
    print('b64Out: ', b64Out)


if __name__ == "__main__":
    main()
