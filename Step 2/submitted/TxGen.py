import math
import random
import string
import sys
import os
import pyprimes
import hashlib
import DSA


# Generate single transaction

def GenSingleTx(p, q, g, alpha, beta):
    serialNum = random.getrandbits(128)
    payer = "Erdem Bozkurt"
    payee = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(10))
    amount = random.randint(1, 10000)
    transaction = '''*** Bitcoin transaction ***
Serial number: %d
Payer: %s
Payee: %s
Amount: %d Satoshi
p: %d
q: %d
g: %d
Public Key (beta): %d
''' % (serialNum, payer, payee, amount, p, q, g, beta)

    r, s = DSA.SignGen(transaction, p, q, g, alpha, beta)
    transaction = transaction + '''Signature (r): %d
Signature (s): %d
''' % (r, s)

    return transaction
