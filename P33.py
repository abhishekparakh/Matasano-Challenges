#Implement Diffie-Hellman
import os
import hashlib
import sys



class Alice:
    '''
    attributes: A, a, keyA
    '''
    def __init__(self, primeP):
        #sys.getsizeof gets the number of bytes in primeP
        random_num = int.from_bytes(os.urandom(sys.getsizeof(primeP)), sys.byteorder)
        self.a = random_num % primeP

    def generatePubKey(self, primeP, generator_g):
        self.A = pow(generator_g, self.a, primeP)
        return self.A

    def generateKey(self, primeP, generator_g, B):
        s = pow(B, self.a, primeP)
        self.keyA = hashlib.sha256(str(s).encode()).hexdigest()
        return self.keyA



class Bob:
    '''
    attributes: B, b, keyB
    '''
    def __init__(self, primeP):
        #sys.getsizeof gets the number of bytes in primeP
        random_num = int.from_bytes(os.urandom(sys.getsizeof(primeP)), sys.byteorder)
        self.b = random_num % primeP

    def generatePubKey(self, primeP, generator_g):
        self.B = pow(generator_g, self.b, primeP)
        return self.B

    def generateKey(self, primeP, generator_g, A):
        s = pow(A, self.b, primeP)
        self.keyB = hashlib.sha256(str(s).encode()).hexdigest()
        return self.keyB



def main():
    primeP = int('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024' \
                'e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd' \
                '3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec' \
                '6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f' \
                '24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361' \
                'c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552' \
                'bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff' \
                'fffffffffffff', base=16)
    generator_g = 2
    alice = Alice(primeP)
    bob = Bob(primeP)

    A = alice.generatePubKey(primeP, generator_g)
    B = bob.generatePubKey(primeP, generator_g)

    #generate keys
    keyA = alice.generateKey(primeP, generator_g, B)
    keyB = bob.generateKey(primeP, generator_g, A)

    print(keyA==keyB)





if __name__ == "__main__":
    main()