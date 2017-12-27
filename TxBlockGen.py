import math
import random, string
import warnings
import sys, os
import pyprimes
import hashlib

def GenTxBlock(p, q, g, count):
    serialNum = random.getrandbits(128)
    amount = random.randint(1, 10000)
    payerPublicKey = random.getrandbits(2048)
    payeePublicKey = random.getrandbits(2048)
    transaction = '''*** Bitcoin transaction ***
Serial number: %d
p: %d
q: %d
g: %d
Payer Public Key (beta): %d
Payee Public Key (beta): %d
Amount: %d Satoshi
''' % (serialNum, p, q, g, payerPublicKey, payeePublicKey, amount)

    r, s = DSA.SignGen(transaction, p, q, g, alpha, beta)
    transaction = transaction + '''Signature (r): %d
Signature (s): %d
''' % (r, s)

    return transaction


if os.path.exists('DSA_params.txt') == True:
    inf = open('DSA_params.txt', 'r')
    q = int(inf.readline())
    p = int(inf.readline())
    g = int(inf.readline())
    inf.close()
    print "DSA parameters are read from file DSA_params.txt"
else:
    print 'DSA_params.txt does not exist'
    sys.exit()
GenTxBlock(p,q,g,1)
