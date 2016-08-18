import string

def mc_part3(idx=15):
    h = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    hh = bytes.fromhex(h)

    for k in string.ascii_letters:
        print(k)
        print(bytes([a ^ b for (a, b) in zip(hh, bytes(k * len(hh), 'ascii'))]))

mc_part3()