import math
import random
import string
import sys
import os
import pyprimes
import hashlib


if sys.version_info < (3, 6):
    import sha3


'''
def DL_Param_Generator(small_bound, large_bound):
    while True:
        while True:
            q = generate_big_prime(256)
            if(small_bound < q < large_bound): break
        print q
        while True:
            p = generate_big_prime(2048)
            if(small_bound < p < large_bound): break
        print p
        if gcd(q, p - 1) != 1:
            break
    alpha = random.randint(1,p)
    g = pow(alpha, (p-1)/q, p)
    return q, p, g
'''
'''
def DL_Param_Generator(small_bound, large_bound):
    while True:
        while True:
            q = generateLargePrime(256)
            if not(small_bound < q < large_bound):
                print "q not between small/large bound"
                break
        print q
        while True:
            p = generateLargePrime(2048)
            if not (small_bound < p < large_bound):
                print "p not between small/large bound"
        print p
        if gcd(q, p - 1) != 1:
            print "gcd(q, p - 1) != 1"
            break
    alpha = random.randint(1,p)
    g = pow(alpha, (p-1)/q, p)
    return q, p, g
'''

def DL_Param_Generator(small_bound, large_bound):
    while True:
        p = generateLargePrime(2048)
        if not (small_bound < p < large_bound):
            print "p not between small/large bound"
        else: break
    print p
    while True:
        q = generateLargePrime(256)
        # if not(small_bound < q < large_bound):
        #     print "q not between small/large bound"
        #     continue
        if gcd(q, p - 1) != 1:
            print "gcd(q, p - 1) == 1, keep p, recalculate q"
            break
    print q
    alpha = random.randint(1,p)
    g = pow(alpha, (p-1)/q, p)
    return q, p, g

def rabinMiller(n):
     s = n-1
     t = 0
     while s&1 == 0:
         s = s/2
         t +=1
     k = 0
     while k<128:
         a = random.randrange(2,n-1)
         #a^s is computationally infeasible.  we need a more intelligent approach
         #v = (a**s)%n
         #python's core math module can do modular exponentiation
         v = pow(a,s,n) #where values are (num,exp,mod)
         if v != 1:
             i=0
             while v != (n-1):
                 if i == t-1:
                     return False
                 else:
                     i = i+1
                     v = (v**2)%n
         k+=2
     return True

def isPrime(n):
     #lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
     #under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
     #of composite numbers from our potential pool without resorting to Rabin-Miller
     lowPrimes =   [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                   ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                   ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                   ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                   ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                   ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                   ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                   ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                   ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                   ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
     if (n >= 3):
         if (n&1 != 0):
             for p in lowPrimes:
                 if (n == p):
                    return True
                 if (n % p == 0):
                     return False
             return rabinMiller(n)
     return False

def generateLargePrime(k):
     #k is the desired bit length
     r=100000*(math.log(k,2)+1) #number of attempts max
     r_ = r
     while r>0:
        #randrange is mersenne twister and is completely deterministic
        #unusable for serious crypto purposes
         n = random.randrange(2**(k-1),2**(k))
         r-=1
         if isPrime(n) == True:
             return n
     return "Failure after "+`r_` + " tries."


'''
# fermat's little theorem


def is_prime(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = random.randint(1, num - 1)
        if pow(val, num - 1, num) != 1:
            return False
    return True


def generate_big_prime(n):
    found_prime = False
    while not found_prime:
        p = random.randint(pow(2,n-1), pow(2,n))
        if is_prime(p, 10):
            return p
'''

def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if a % b == 0:
        return b
    return gcd(b, a % b)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# a, b, c = DL_Param_Generator(256, 64)
# print a, b, c

# Key generation


def KeyGen(p, q, g):
    alpha = random.randint(1, q - 1)
    beta = pow(g, alpha, p)
    return alpha, beta

# Signature generation


def SignGen(m, p, q, g, alpha, beta):
    h = int(hashlib.sha3_256(m).hexdigest(),16)
    h = h % q
    k = random.randint(1, q - 1)
    r = pow(g, k, p)
    s = ((alpha * r) + (k * h)) % q
    return r, s

# Signature verification


def SignVer(m, r, s, p, q, g, beta):
    h = int(hashlib.sha3_256(m).hexdigest(),16)
    h = h % q
    #pow (g,w,p) -> pow(modinv(g,p),w,p)
    v = pow(modinv(h,q),1,q)
    #v = pow(h,-1,q) won't work
    z1 = (s * v) % q
    z2 = ((q - r) * v) % q
    #u = (pow(g, z1) * pow(beta, z2)) % p
    u = (pow(g,z1,p)*pow(beta,z2,p)) %p
    if(r % q == u % q):
        return 1
    else:
        return 0
