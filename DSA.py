import math
import random
import string
import sys
import os
import pyprimes
import hashlib

if sys.version_info < (3, 6):
    import sha3


def DL_Param_Generator(small_bound, large_bound):
    g = 1
    while True:
        q = generate_big_prime(small_bound)
        p = generate_big_prime(large_bound)
        if gcd(q, p - 1) != 1:
            break
    file = open("TEST_params.txt", "w")
    file.write(str(q))
    file.write("\n")
    file.write(str(p))
    file.write("\n")
    file.write(str(g))
    file.close()
    return q, p, g



#from random import randint
randint = random.randint

# fermat's little theorem


def is_prime(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = randint(1, num - 1)
        if pow(val, num - 1, num) != 1:
            return False
    return True


def generate_big_prime(n):
    found_prime = False
    while not found_prime:
        p = randint(2**(n - 1), 2**n)
        if is_prime(p, 1000):
            return p


def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if a % b == 0:
        return b
    return gcd(b, a % b)


a, b, c = DL_Param_Generator(256, 64)
print a, b, c

# Key generation


def KeyGen(p, q, g):
    alpha = random.rantint(0, q - 1)
    beta = pow(g, alpha, p)
    return alpha, beta

# Signature generation


def SignGen(m, p, q, g, alpha, beta):
    hash = hashlib.sha3_256(m).hexdigest()
    h = h % q
    k = random.rantint(0, q - 1)
    r = pow(g, k, p)
    s = (alpha * r) + ((k * h) % q)
    return r, s

# Signature verification


def SignVer(m, r, s, p, q, g, beta):
    h = hashlib.sha3_256(m).hexdigest()
    h = h % q
    v = (1 / h) % q
    z1 = (s * v) % q
    z2 = ((q - r) * v) % q
    u = (pow(g, z1) * pow(beta, z2)) % p
    if(r == u % q):
        return 1
    else:
        return 0
